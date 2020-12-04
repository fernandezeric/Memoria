
import Freya.catalogs # __path__ # dir modules
import os

class Verify():

    """
    """
    def verify_catalog_inside(self,name):
        self.name = name
        dir_catalogs = Freya.catalogs.__path__[0]
        if self.name  in os.listdir(dir_catalogs) :
             return True 
        return False

    """
    """
    def verify_catalog_local(self,name):
        self.name = name
        try :
            mod = importlib.import_module('LocalCatalogs.catalogs')
            dir_catalogs = mod.__path__[0]
            if self.name  in os.listdir(dir_catalogs) :
                return True 
            return False
        except:
            return False
    """
    """  
    def verify_source(self,source):
        self.source = source
        if self.source not in ['api']:
            return True
        return False

    """
    """
    def verify_format(self,format):
        self.format = format
        if self.format not in ['csv']:
            return True
        return False