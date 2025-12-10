import ffmpeg
import argparse
import json
from pathlib import Path
import logging
import re 
import os
import threading 
import datetime
import random
import string
from typing import List

# TODO
# For the CLI tool, add a verification mechanism on timestamps : if a timestamp is mm:ss instead
# of hh:mm:ss add 00 or 01 depending on the total duration of video and/or the previous clip timestamp

logging.getLogger().setLevel(logging.DEBUG)

class Clip:
    def __init__(self,s : str,e :str):
        
        self.Start : str = ""
        self.End  : str = ""
        self.Path : str = ""
        
        s = s.strip(" ")
        e = e.strip(" ")

        if len(s) == 0 or len(e) == 0:
            logging.error(f"Got an empty timestamp when constructing clip : start {s}   end {e} ")
            raise ValueError

        if re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", s):
            self.Start = s
        else :
            logging.critical(f"{s} for start timestamp in not valid")

        if re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", e):
            self.End = e
        else :
            logging.critical(f"{e} for end timestamp in not valid")
    
        self.Path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".mp4"


class Video:

    def __init__(self,t : str):
        if len(t) == 0 :
            logging.error("Did not get a string with a title")
            raise ValueError
        self.Clips : List[Clip] = []
        self.Title = t

    def AddClip(self, c: Clip):
        self.Clips.append(c)

class ParamFile:

    def __init__(self):
        self.Data : List[Video] = []
        
    def AddVideo(self, v: Video):
        if len(v.Clips) != 0:
            self.Data.append(v)

def handleExistingFolder(path: str):
    cont = ""
    while cont not in ["y","Y","n","N"]:
        cont = input(f"The repertory {path} already exists, existing file will be overwritten, continue [y/n] :")
    if cont not in ["y","Y"]:
        exit(1)
    
    return

def create_video(FOLDER_NAME, base_video_path: str, v : Video):
    logging.info(f"Creating new video {v.Title}")
    # prepare the output repository
    temp_path = Path(FOLDER_NAME+"/.temp").absolute()
    if not temp_path.exists():
        temp_path.mkdir()
    
    new_vid_path = Path(f"{FOLDER_NAME}/{v.Title}.mp4")
    base_stream = ffmpeg.input(base_video_path)
    logging.info(f"Trimming video for {v.Title}")
    trim_start = datetime.datetime.now()
    for c in v.Clips:
        logging.debug(c.Path)
        try:
            (
            ffmpeg
                .input(base_video_path,ss=c.Start,to=c.End)
                .output(temp_path.__str__()+"/"+c.Path,c="copy")
                .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )    
        except ffmpeg.Error as e:
            logging.error(f"Error when trimining video {v.Title} \n Timestamps : {c.Start} - {c.End} \nError : {e.stderr.decode("utf-8") if e.stderr else "No error message"}")
            return
        except Exception as e:
            logging.error(f"Something bad happened  when trimining video {v.Title} \nError : {str(e)}")

        
        with open(temp_path.__str__()+"/concats.txt","a+") as f:
            f.write(f"file '{temp_path.__str__()+"/"+c.Path}'\n")
            f.close()
            
    logging.info(f"Finished trimming in {datetime.datetime.now() - trim_start} for {v.Title}")
    
    concat_start = datetime.datetime.now()
    try:
        (
            ffmpeg
            .input(temp_path.__str__()+"/concats.txt", format="concat", safe=0)
            .output(filename=new_vid_path,c="copy")
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e :
        logging.error(f"Error when concatenating video {v.Title} \nError : {e.stderr.decode("utf-8") if e.stderr else "No error message"}")
        return
    except Exception as e:
        logging.error(f"Something bad happened when concatenating video {v.Title} \nError : {str(e)}")
        return
    
    logging.info(f"Finished outputing in {datetime.datetime.now() - concat_start} for {v.Title}")
 
parser = argparse.ArgumentParser(prog="replay editor",description="using a json with video names and timestamps for each actions, create each video")
parser.add_argument("-v", required=True, help="Path to the video you want to extract clips from")
parser.add_argument("-j", required=True, help="Path to the JSON file holding the timestamps")
parser.add_argument("-o", required=True, help="Name of the repertory where clips will be created")


args = parser.parse_args()
if not Path(args.v).exists():
    logging.fatal(f"Provided path {args.v} to video file is not found")
if not Path(args.j).exists():
    logging.fatal(f"Provided path {args.j} to JSON file is not found")
if Path(args.o).exists():    
    handleExistingFolder(args.o)

FOLDER_NAME = args.o
base_video_path = args.v
recapFile = ParamFile()
with open(args.j) as f:
    data = f.read()
    d = json.loads(data)
    for video in d :
        try: 
            title = list(dict.keys(video))[0]
            v = Video(title)
        except ValueError:
            logging.fatal(f"Did not find a title in this video object : {video}")
        for clip in video[title]:
            try:
                v.AddClip(Clip(clip["debut"], clip["fin"]))
            except ValueError:
                logging.fatal(f"Error in video {title}")
                exit()
        recapFile.AddVideo(v)
    
    f.close()

if not Path(FOLDER_NAME).exists():
    os.mkdir(FOLDER_NAME)
    logging.info(f"Created folder {FOLDER_NAME}")

threads = []
for v in recapFile.Data:
    t = threading.Thread(target=create_video,args=(FOLDER_NAME,base_video_path,v))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
    
    

