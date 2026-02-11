from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QSlider, QSizePolicy
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl
from models.configuration import Configuration
from ffmpeg import probe
from datetime import timedelta
from utils import time_conversions as tc
import logging

class VideoWidget(QWidget):
    def __init__(self, conf : Configuration):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Added this to have focus with key pressed
        self.video_player_layout = QVBoxLayout()
        self.setLayout(self.video_player_layout)
        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile(conf.inputVideo))
        self.video_widget = QVideoWidget()
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.video_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.media_player.setVideoOutput(self.video_widget)
        

        self.media_player.play()
        self.media_player.setPosition(0)
        self.media_player.pause()        

        self.video_player_layout.addWidget(self.video_widget)
        
        self.video_timeline = QSlider()
        self.video_timeline.setOrientation(Qt.Orientation.Horizontal)
        self.video_timeline.setMaximum(get_video_duration(conf.inputVideo))
        
        
        self.video_total_time_ms = str(timedelta(milliseconds=self.video_timeline.maximum())) 
        self.video_hhmmss_lenght = self.video_total_time_ms.split(".")[0]
    
        self.current_time_lbl = QLabel(f"00:00:00 / {self.video_hhmmss_lenght}")

        # Updates the other widget when the video play
        self.media_player.positionChanged.connect(self.change_time_label)
        self.media_player.positionChanged.connect(self.change_video_timeline)
        
        # Handles the moving of the time slider by the user
        self.video_timeline.sliderMoved[int].connect(self.change_video_frame)
        self.video_timeline.valueChanged[int].connect(self.change_video_frame)
            
        self.timeline_layout = QHBoxLayout()
        self.timeline_layout.addWidget(self.current_time_lbl)
        self.timeline_layout.addWidget(self.video_timeline)
        self.video_player_layout.addLayout(self.timeline_layout)
        
    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        logging.debug(f"What has been pressed: {a0.key()}")
        if a0.key() == Qt.Key.Key_Right:
            self.forward_video(5000)
        elif a0.key() == Qt.Key.Key_Left:
            self.backward_video(5000)
        elif a0.key() == Qt.Key.Key_Space:
            logging.debug("Key space is pressed")
            if self.media_player.isPlaying():
                self.media_player.pause()
            else :
                self.media_player.play()

        
    def change_time_label(self,value):        
        hhmmss_time = tc.Timestamp_to_hhmmss(value)
        self.current_time_lbl.setText(f"{hhmmss_time} / {self.video_hhmmss_lenght}")
        
    def change_video_frame(self,value):
        print(f"\n\n value {value}")
        self.media_player.pause()
        self.media_player.setPosition(value)
        self.media_player.play()
        
    def forward_video(self, duration: int):
        # self.media_player.pause()
        self.media_player.setPosition(self.media_player.position() + duration)
        # self.media_player.play()
    
    def backward_video(self, duration: int):
        # self.media_player.pause()
        self.media_player.setPosition(self.media_player.position() - duration)
        # self.media_player.play()
        
    def change_video_timeline(self,value):
        self.video_timeline.blockSignals(True)
        self.video_timeline.setSliderPosition(value)
        self.video_timeline.blockSignals(False)

def get_video_duration(path: str) -> int:
    json_info = probe(path)
    duration_sec = json_info["format"]["duration"]
    duration_ms = float(duration_sec) *1000
    
    return duration_ms.__round__()
