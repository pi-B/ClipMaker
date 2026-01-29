import logging
import re
import random
import string

class Clip:
    # s (start time) and e (end time) must be in the %H:%M:%S format
    def __init__(self,s : str,e : str = None):
        
        self.Start : str = ""
        self.End  : str = ""
        self.Path : str = ""
        
        s = s.strip(" ")
        self.Add_start(s)
        
        if e is not None and len(e) != 0:
            e = e.strip(" ")
            self.Add_end(e)
    
        self.Path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".mp4"

    def Add_end(self, e : str):
        e = e.strip(" ")
        if re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", e):
            
            self.End = e
        else :
            logging.critical(f"{e} for end timestamp in not valid")
            raise ValueError
        
    def Add_start(self, s: str):
        
        if len(s) != 0:
            if re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", s):
                self.Start = s
            else :
                logging.critical(f"{s} for start timestamp in not valid")
                raise ValueError
    
    def set_path(self):
        if len(self.Path) == 0:
            self.Path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".mp4"