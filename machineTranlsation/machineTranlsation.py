
# coding: utf-8

# In[ ]:



from __future__ import division
import logging
import os
import xml.etree.ElementTree as ET

from senpy.plugins import SenpyPlugin
from senpy.models import Results, Entry

logger = logging.getLogger(__name__)

# my packages


class machineTranlsation(SenpyPlugin):
    
    def __init__(self, info, *args, **kwargs):
        super(machineTranlsation, self).__init__(info, *args, **kwargs)
        self.name = info['name']
        self.id = info['module']
        self._info = info
        local_path=os.path.dirname(os.path.abspath(__file__))

        
        

    def activate(self, *args, **kwargs):
        
        st = datetime.now()
        
        logger.info("{} {}".format(datetime.now() - st, "active"))


        logger.info("machineTranlsation plugin is ready to go!")
        
    def deactivate(self, *args, **kwargs):
        try:
            logger.info("machineTranlsation plugin is being deactivated...")
        except Exception:
            print("Exception in logger while reporting deactivation of machineTranlsation")

    #MY FUNCTIONS
    
    
    
    def _bind_vectors(self, x):
        return np.concatenate(x)  
   
    
    def analyse(self, **params):
        logger.debug("Hashtag SVM Analysing with params {}".format(params))
                
        text_input = params.get("input", None)
        self.__source = params.get("sourcelanguage", 'en')
        self.__target = params.get("targetlanguage", 'es')
                    
            
        response = Results()

        entry = Entry()
        entry.nif__isString = text_input

        entry['nif:translation'] = text_input
        
        response.entries.append(entry)
        # entry.language = lang
            
        return response

