from typing import Dict, List, Tuple
from pathlib import Path
import json
import os
from enum import Enum
import logging
from models.clips import Clip

class FileState(Enum):
    CREATED = 1
    EXISTS  = 2

class AutoSaver():
    
    def __init__(self):
        pass
    
    def __init__(self,output_dir : str, categories : list[str]):
        self.AUTOSAVER_FILE_NAME = "auto_save.json"
        self.output_dir = output_dir
        self.categories_dict : Dict[str, List[Tuple[str,str]]] = {} 
        
        self.init_autosaver_file()
        if self.file_state == FileState.EXISTS:
            logging.debug("retrieving saved clips")
            with open(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME, "r") as file:
                existing_data = json.loads(file.read())
                logging.debug(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME)
                logging.debug(existing_data)
                cat_dict = existing_data["clips"]
                for cat in cat_dict.keys():
                    self.categories_dict[cat] = []
                    for clip in cat_dict[cat]:
                        self.categories_dict[cat].append(clip)
            
                    
                    
    def init_autosaver_file(self):
        autosaver_file = self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME
        if not Path(autosaver_file).exists():
            if not Path(self.output_dir + ".project/").exists():
                os.mkdir(self.output_dir + ".project/")
            with open(autosaver_file, "w") as file:
                d = dict()
                json.dumps(d)
                file.write(json.dumps(d))
                file.close()
            self.file_state = FileState.CREATED
        else :
            self.file_state = FileState.EXISTS
                
    def add_clip(self, category : str, clip : Clip):
        if self.categories_dict.get(category) is not None :
            self.categories_dict[category].append(tuple(clip.Start, clip.End))
        else:
            self.categories_dict[category] = [(clip.Start, clip.End)] 
        logging.debug(f"added new clip to {category} : start {clip.Start} end {clip.End}")
        self.dump_data()
            
    
    def dump_data(self):
        with open(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME, "w") as file:
            file.write(json.dumps(self.categories_dict))
            logging.debug("dumped data")
    
    def get_restart() -> bool :
        # create a state file in a hidden file
        # read the state file
        # return running == false
        return True