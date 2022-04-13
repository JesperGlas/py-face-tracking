import PySimpleGUI as psg
import cv2

TITLE : str = 'Face Tracking'
VERSION : str = '1.0.0'
    
def initLayout() -> list:
    return [
        [psg.Image(key = '-IMAGE-')],
        [psg.Text('People in frame: 0', key = '-TEXT-', expand_x = True, justification = 'c')]
    ]

# initLayout
    
def run():
    layout : list = initLayout()
    
    window = psg.Window(f'{TITLE} - v{VERSION}', layout)

    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            break
        
    window.close()

# run

def main():
    print(f'Loading {TITLE} v{VERSION}...')
    
    run()
    
# main
    
if __name__ == '__main__':
    main()