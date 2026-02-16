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
    
    def __init__(self,output_dir : str, input_video : str, project_name: str):
        self.AUTOSAVER_FILE_NAME = "auto_save.json"
        self.output_dir = output_dir
        self.categories_dict : Dict[str, List[Tuple[str,str]]] = {} 
        
        self.init_autosaver_file()
        if self.file_state == FileState.EXISTS:
            with open(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME, "r+") as file:
                existing_data = json.loads(file.read())
                logging.debug("retrieving saved clips")
                logging.debug(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME)
                logging.debug(existing_data)
                cat_dict = existing_data.get("clips")
                if cat_dict is not None: 
                    for cat in cat_dict.keys():
                        self.categories_dict[cat] = []
                        for clip in cat_dict[cat]:
                            self.categories_dict[cat].append(clip)
                file.close()
                
        if self.file_state == FileState.CREATED:
            with open(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME, "w") as file:
                new_data = {}
                new_data["project_name"] = project_name
                new_data["input_video"] = input_video
                new_data["clips"] = {}
                file.write(json.dumps(new_data))
                file.close()
            
                    
                    
    def init_autosaver_file(self):
        autosaver_file = self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME
        if not Path(autosaver_file).exists():
            if not Path(self.output_dir + ".project/").exists():
                os.mkdir(self.output_dir + ".project/")
                logging.debug("created the .project directory")
            with open(autosaver_file, "w") as file:
                file.write("{}")
                file.close()
                logging.debug("created the auto-save file")
            self.file_state = FileState.CREATED
        else :
            self.file_state = FileState.EXISTS
                
    def add_clip(self, category : str, clip : Clip):
        if self.categories_dict.get(category) is not None :
            self.categories_dict[category].append((clip.Start, clip.End))
        else:
            self.categories_dict[category] = [(clip.Start, clip.End)] 
        logging.debug(f"added new clip to {category} : start {clip.Start} end {clip.End}")
        self.write_data()
    
    def remove_clip(self, category: str, removed_clip : Clip):
        if self.categories_dict.get(category) is not None :
            for i in range(0,len(self.categories_dict[category])-1):
                clip = self.categories_dict[category][i]
                if clip[0] == removed_clip.Start and clip[1] == removed_clip.End:
                    self.categories_dict[category].pop(i)
                    break
        logging.debug(f"removed clip from {category} : start {removed_clip.Start} end {removed_clip.End}")
        self.write_data()
        
    
    def write_data(self):
        current_data = self.get_auto_save_data()
        with open(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME, "w") as file:
            current_data["clips"] = self.categories_dict
            file.write(json.dumps(current_data))
            logging.debug("dumped data")
    
    def get_restart() -> bool :
        # create a state file in a hidden file
        # read the state file
        # return running == false
        return True
    
    def get_auto_save_data(self) -> dict :
        with open(self.output_dir + ".project/" + self.AUTOSAVER_FILE_NAME, "r") as file:
            data_str = file.read()
            return json.loads(data_str)