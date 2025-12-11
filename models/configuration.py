from typing import List
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Configuration:
    
    def __init__(self):
        
        self.projectName = ""
        self.inputVideo = ""
        self.outputDirectory = ""
        
        self.preconfiguredCategories : List[str] = []
        
    def isReady(self):
        logging.debug(f"name : {self.projectName} input: {self.inputVideo}. output: {self.outputDirectory}")
        return len(self.projectName) != 0 and len(self.inputVideo) != 0 and len(self.outputDirectory) != 0