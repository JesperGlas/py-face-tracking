import PySimpleGUI as psg

TITLE : str = 'Face Tracking'
VERSION : str = '1.0.0'
    
def initLayout() -> list:
    return [
        [psg.Text(f'{TITLE} - {VERSION}')],
        [psg.Button('Test')],
        [psg.Input()]
    ]

# initLayout
    
def app():
    layout : list = initLayout()
    
    psg.Window('Face Tracking', layout).read()

# app

def main():
    print(f'Loading {TITLE} v{VERSION}...')
    
    app()
    
# main
    
if __name__ == '__main__':
    main()