from datetime import datetime
from datetime import timedelta
from PyQt6.QtWidgets import QLabel

def Hhmmss_to_timestamp(time : str) -> int :
    value = datetime.strptime(time, "%H:%M:%S")
    res = value.hour * 3600000 + value.minute * 60000 + value.second * 1000 
    return int(res)

def Timestamp_to_hhmmss(time : int) -> str :
    
    value = timedelta(milliseconds=time)
    dd = datetime.strptime(str(value).split(".")[0],"%H:%M:%S")
    return datetime.strftime(dd,"%H:%M:%S")

# Extract the first part of a QLabel's text in the 'hh:mm:ss / hh:mm:ss' format and return it a `str`
def Extract_hhmmss_from_label(label : QLabel) -> str:
    txt = label.text().strip(" ")
    time = txt.split("/")[0]
    return time
    