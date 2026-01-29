from typing import List
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Configuration:
    
    def __init__(self) -> None:
        
        self.projectName: str = ""
        self.inputVideo: str = ""
        self.outputDirectory: str = ""
        
        self.preconfiguredCategories : List[str] = []
        
    def isReady(self) -> bool:
        logging.debug(f"name : {self.projectName} input: {self.inputVideo}. output: {self.outputDirectory}")
        return len(self.projectName) != 0 and len(self.inputVideo) != 0 and len(self.outputDirectory) != 0