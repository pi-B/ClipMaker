from models.clips import Clip
from models.video import Video
import logging
import os
from pathlib import Path
from datetime import datetime
import ffmpeg


def create_video(output_folder: str, base_video_path: str, v : Video):
    logging.info(f"Creating new video {v.Title}")
    # prepare the output repository
    if not Path(output_folder).absolute().exists():
        Path(output_folder).absolute().mkdir()
        
    temp_path = Path(output_folder+"/.temp/").absolute()
    if not temp_path.exists():
        temp_path.mkdir()
    
    new_vid_path = Path(f"{output_folder}/{v.Title}.mp4")
    logging.info(f"Trimming video for {v.Title}")
    trim_start = datetime.now()
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
            logging.error(f"Error when trimining video {v.Title} \n Timestamps : {c.Start.replace(" ", "␣")} - {c.End.replace(" ", "␣")} \nError : {e.stderr.decode("utf-8") if e.stderr else "No error message"}")
            return
        except Exception as e:
            logging.error(f"Something bad happened  when trimining video {v.Title} \nError : {str(e)}")
            return
        
        with open(temp_path.__str__()+"/concats.txt","a+") as f:
            f.write(f"file '{temp_path.__str__()+"/"+c.Path}'\n")
            f.close()
            
    logging.info(f"Finished trimming in {datetime.now() - trim_start} for {v.Title}")
    
    
    concat_start = datetime.now()
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
    
    logging.info(f"Finished outputing in {datetime.now() - concat_start} for {v.Title}")
    clean_output_directory(output_folder)
    
def clean_output_directory(output_folder: str):
    temp_dir = Path(output_folder + "/.temp")
    if temp_dir.exists():
        for p in sorted(temp_dir.glob('**/*') , reverse=True):
            if not p.exists():
                continue
            p.chmod(0o666)
            if p.is_dir():
                p.rmdir()
            else:
                p.unlink()
        
        try:
            temp_dir.rmdir()
        except OSError as e:
            logging.error(f"Could not delete {temp_dir} : {e=}")
        logging.info("successfully removed the temporary folder")
 