import PySimpleGUI as psg
import cv2

TITLE : str = 'Face Tracking'
VERSION : str = '1.0.0'

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
    face_cascade = cv2.CascadeClassifier('./assets/opencv_cascades/haarcascade_frontalface_default.xml')

    # Main loop
    while True:
        event, values = window.read(timeout = 0)
        if event == psg.WIN_CLOSED:
            break
        
        # Video
        arg, frame = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor = 1.3,
            minNeighbors = 7,
            minSize = (50, 50)
        )
                
        # Draw rectangle on faces
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame, 
                (x, y), (x + w, y + h),
                (0, 255, 0), 2
            )

        # Update the image
        imgbytes = cv2.imencode('.png', frame)[1].tobytes() # Index 1 is image data
        window['-IMAGE-'].update(data = imgbytes)
        
        # Update window text
        window['-TEXT-'].update(f'People: {len(faces)}')
    
    # Shutdown
    window.close()

# run

def main():
    print(f'Loading {TITLE} v{VERSION}...')
    
    run()
    
# main
    
if __name__ == '__main__':
    main()