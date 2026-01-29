from typing import List
import logging
from models.clips import Clip

class Video:

    def __init__(self,t : str):
        if len(t) == 0 :
            logging.error("Did not get a string with a title")
            raise ValueError
        self.Clips : List[Clip] = []
        self.Title = t

    def AddClip(self, c: Clip):
        self.Clips.append(c)
