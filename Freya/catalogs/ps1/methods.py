"""
In this file you can created methods for 'configure.py'  
"""
import requests
import io
from Freya.core import utils


from astropy.io import ascii
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u


class Methods_ps1():

    def __init__(self,**kwargs):
        self.ra = kwargs.get('ra')
        self.dec = kwargs.get('dec')
        self.radius = kwargs.get('radius')
        self.format = kwargs.get('format')
        self.nearest = kwargs.get('nearest')

    def ps1cone(self,table="mean",release="dr1",format="csv",columns=None,
            baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",
            **kw):
        """Do a cone search of the PS1 catalog
        Parameters
        ----------
        """
        data = kw.copy()
        data['ra'] = self.ra
        data['dec'] = self.dec
        data['radius'] = self.radius
        return self.ps1search(table=table,release=release,format=self.format,columns=columns,
                        baseurl=baseurl, **data)

    #https://ps1images.stsci.edu/ps1_dr2_api.html
    def ps1search(self,format,table="mean",release="dr1",columns=None,
            baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",
            **kw):
        """Do a general search of the PS1 catalog (possibly without ra/dec/radius)
        
        Parameters
        ----------
        """
        data = kw.copy()
        url = f"{baseurl}/{release}/{table}.{format}"
        data['columns'] = '[{}]'.format(','.join(columns))
        # either get or post works
        r = requests.get(url, params=data)
        r.raise_for_status()
        if format == "json":
            return r.json()
        else:
            return r.text

    def ps1ids(self):
        """Get ids (ps1 id) of objects in a radius with respect to ra and dec
        Parameters
        ----------
        """
        constraints = {'nDetections.gt':1}
        columns = ['objID','raMean','decMean']
        results = self.ps1cone(self.ra,self.dec,self.radius,release='dr2',columns=columns,**constraints)


        # if results.status_code != '200': 
        #     return -99 #'not found' # change to more general

        if len(results) <= 0: # if no return some object
            return -1

        results = ascii.read(results)


        if self.nearest is True:
            angle = []
            c1 = SkyCoord(ra=self.ra,dec=self.dec,unit=u.degree)
            for re in results:
                c2 = SkyCoord(ra=re['raMean'],dec=re['decMean'],unit=u.degree)
                angle.append(c1.separation(c2))
            minps1 = angle.index(min(angle))
            #temporal 4 meses de temporal xD
            temp = []
            temp.append(results[minps1]['objID'])
            return temp

        else :
            return results['objID']


    def ps1curves(self):
        """Get light curves of objects in specific radio with respect ra and dec, and possible return the object most nearest to radio
        Parameters
        ----------
        """
        ids = self.ps1ids(self.ra,self.dec,self.radius,self.nearest)
        ps1dic = {}
        if ids == -1:
            ps1dic['0'] = 'not found' # not object find
            return ps1dic
        # #when request failed in api
        # elif ids == -99: 
        #     ps1dic['not found'] = 'result.status_code '
        #     return ps1dic

        for id in ids:
            dconstraints = {'objID': id}
            dcolumns = ("""objID,detectID,filterID,obsTime,ra,dec,psfFlux,psfFluxErr,psfMajorFWHM,psfMinorFWHM,
                        psfQfPerfect,apFlux,apFluxErr,infoFlag,infoFlag2,infoFlag3""").split(',')
            dcolumns = [x.strip() for x in dcolumns]
            dcolumns = [x for x in dcolumns if x and not x.startswith('#')]
            dresults = self.ps1search(format,table='detection',release='dr2',columns=dcolumns,**dconstraints)
            if(format == 'csv'):
                dresults = ascii.read(dresults)
                buf = io.StringIO()
                ascii.write(dresults,buf,format='csv')
                ps1dic[str(id)] =  buf.getvalue()
            else :
                ps1dic[str(id)] = dresults
        return ps1dic