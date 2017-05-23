
# coding: utf-8

# In[ ]:



from __future__ import division
import logging
import os
import xml.etree.ElementTree as ET

from senpy.plugins import SenpyPlugin, EmotionPlugin
from senpy.models import Results, Entry, Error

logger = logging.getLogger(__name__)

import numpy as np
import math, itertools
from collections import defaultdict

import gzip
from datetime import datetime 
import subprocess



class machineTranslation(EmotionPlugin):
    
    def __init__(self, info, *args, **kwargs):
        super(machineTranslation, self).__init__(info, *args, **kwargs)
        self.name = info['name']
        self.id = info['module']
        self._info = info
        local_path = os.path.dirname(os.path.abspath(__file__))
   
        

    def activate(self, *args, **kwargs):
        
        st = datetime.now()        
        logger.info("{} {}".format(datetime.now() - st, "active"))
        
        st = datetime.now()        
        subprocess.run(['rm','-f', 'translate.perl'])
        subprocess.run( ['wget','http://server1.nlp.insight-centre.org/docker/translate.perl','-O','translate.perl'] )
        subprocess.run( ['chmod','+x','translate.perl'] )   
        logger.info("{} {}".format(datetime.now() - st, "translation script downloaded"))
        
        logger.info("%s plugin is ready to go!" % self.name)
        
    def deactivate(self, *args, **kwargs):
        try:
            logger.info("%s plugin is being deactivated..." % self.name)
        except Exception:
            print("Exception in logger while reporting deactivation of %s" % self.name)
    
    
    ## CUSTOM METHODS
    
    def _test_method(self):
            result = subprocess.run(['ls', '-la'], stdout=subprocess.PIPE)
            for x in result.stdout.decode("utf-8").split('\n'):
                print(x) 
    
    def _translate(self, source_language_code, target_language_code, text_input):
        
        st = datetime.now() 
        
        command = './translate.perl %s %s "%s"' % (source_language_code, target_language_code, text_input)
        logger.info("executing '%s'" % command)       
        
#         command = './translate.perl£££%s£££%s£££"%s"' % (source_language_code, target_language_code, text_input)
        command = ['./translate.perl', str(source_language_code), str(target_language_code), str(text_input)]
        
        result = subprocess.run( command, stdout=subprocess.PIPE )
        
        logger.info("{} {}".format(datetime.now() - st, "translation is complete"))
        
        result = result.stdout.decode("utf-8")    
        logger.info("\n\n\n"+result+"\n\n\n")
        
        return result

    def analyse(self, **params):      
        
        logger.debug("machine translation with params {}".format(params))
                
        text_input = params.get("input", None)
        source_language_code = params.get("sourcelanguage", None)
        target_language_code = params.get("targetlanguage", None)

        if source_language_code == target_language_code:
            text_output = text_input
        elif 'en' in [source_language_code, target_language_code]:
            text_output = str(self._translate(source_language_code, target_language_code, text_input))
        else:
            raise Error("Unavailable language pair")
            
        response = Results()
        entry = Entry()        
        
        entry.nif__isString = text_input  
        entry['nif:predLang'] = source_language_code
    
        translation = {}        
        translation['nif:isString'] = text_output
        translation['nif:predLang'] = target_language_code
        translation['nif:wasTranslatedFrom'] = entry.id     
        
        entry['nif:translation'] = [translation]
        
        response.entries.append(entry)
            
        return response

