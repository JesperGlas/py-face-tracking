from genericpath import exists
from xmlrpc.client import boolean
import PySimpleGUI as psg # Used for GUI
import cv2 # Used for face tracking
from dataclasses import dataclass
from typing import Dict

@dataclass
class DetectionContext:
    m_Name: str
    m_Cascade: object
    m_Show: bool
    m_RectColor = (0, 255, 0)
    m_ScaleFactor = 1.3
    m_MinNeighbors = 7
    m_MinSize = (50, 50)
    
    def __init__(
        self,
        name: str,
        cascade: str,
        show: bool = False,
        rect_color: tuple = (0, 255, 0),
        scale_factor: float = 1.3,
        min_neighbors: int = 7,
        min_size: tuple = (50, 50)
        ):
        self.m_Name = name
        self.m_Cascade = cascade
        self.m_Show = show
        self.m_RectColor = rect_color
        self.m_ScaleFactor = scale_factor
        self.m_MinNeighbors = min_neighbors
        self.m_MinSize = min_size
        

# Global variables
TITLE : str = 'Face Tracking'
VERSION : str = '1.0.0'

# Inits the contexts for detection
def initDetectionContexts() -> list:    
    return [
        DetectionContext(
            "Front Face",
            cv2.CascadeClassifier('./assets/opencv_cascades/haarcascade_frontalface_default.xml'),
            show=True
        ),
        DetectionContext(
            'Profile Face',
            cv2.CascadeClassifier('./assets/opencv_cascades/haarcascade_profileface.xml'),
            rect_color = (255, 0, 0),
            show=True
        ),
        DetectionContext(
            'Eyes',
            cv2.CascadeClassifier('./assets/opencv_cascades/haarcascade_eye.xml'),
            rect_color=(0, 0, 255),
            min_size=(10, 10),
            show=False
        )
    ]

# initDetectionContexts

# Inits the layout of the window
def initLayout() -> list:
    return [
        [psg.Image(key = '-IMAGE-')],
        [psg.Text('People in frame: 0', key = '-TEXT-', expand_x = True, justification = 'c')]
    ]

# initLayout
    
def run():
    layout : list = initLayout()
    
    # Init window
    window = psg.Window(f'{TITLE} - v{VERSION}', layout)

    # Init video capture
    video = cv2.VideoCapture(0) # 0 = webcam

    # Main loop
    while True:
        event, values = window.read(timeout = 0)
        if event == psg.WIN_CLOSED:
            break
        
        # Video
        arg, frame = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in all contexts
        detection_res: dict = {} # dict to hold the results of the detection
        
        for suite in initDetectionContexts(): # detect for each context
            suite_res = suite.m_Cascade.detectMultiScale(
                gray_frame,
                scaleFactor = suite.m_ScaleFactor,
                minNeighbors = suite.m_MinNeighbors,
                minSize = suite.m_MinSize
            )
            
            # Draw detected areas with rectangles based on m_Show variable
            if suite.m_Show:
                for (x, y, w, h) in suite_res:
                    cv2.rectangle(
                        frame,
                        (x, y), (x + w, y + h),
                        suite.m_RectColor,
                        2
                    )
            
            detection_res[suite.m_Name] = suite_res

        # Update the image
        imgbytes = cv2.imencode('.png', frame)[1].tobytes() # Index 1 is image data
        window['-IMAGE-'].update(data = imgbytes)
        
        # Update window text
        window_text: str = ""
        for key, res in detection_res.items():
            window_text += f'{key}: {len(res)}\n'
            
        window['-TEXT-'].update(window_text)
    
    # Shutdown
    window.close()

# run

def main():
    print(f'Loading {TITLE} v{VERSION}...')
    run()
    
# main
    
if __name__ == '__main__':
    main()