# -*- coding: utf-8 -*-

from __future__ import division
import logging
import os
import xml.etree.ElementTree as ET

from senpy.plugins import EmotionPlugin, SenpyPlugin
from senpy.models import Results, EmotionSet, Entry, Emotion

logger = logging.getLogger(__name__)

# my packages


class machineTranlsation(EmotionPlugin):
    
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

        emotionSet = EmotionSet()
        emotionSet.id = "Emotions"

        emotion1 = Emotion()        

        for dimension in ['V','A','D']:
            weights = [feature_text[i] for i in feature_text if (i != 'surprise')]
            if not all(v == 0 for v in weights):
                value = np.average([self.centroids[i][dimension] for i in feature_text if (i != 'surprise')], weights=weights) 
            else:
                value = 5.0
            emotion1[self._centroid_mappings[dimension]] = value         

        emotionSet.onyx__hasEmotion.append(emotion1)    
        
        for i in feature_text:
            if(self.ESTIMATOR == 'SVC'):
                emotionSet.onyx__hasEmotion.append(Emotion(onyx__hasEmotionCategory=self._wnaffect_mappings[i],
                                    onyx__hasEmotionIntensity=feature_text[i]))
            else:
                if(feature_text[i] > 0):
                    emotionSet.onyx__hasEmotion.append(Emotion(onyx__hasEmotionCategory=self._wnaffect_mappings[i]))
        
        entry.emotions = [emotionSet,]
        
        response.entries.append(entry)
        # entry.language = lang
            
        return response
