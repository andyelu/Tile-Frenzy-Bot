import cv2
import numpy as np
import mss
from bot import TileBot
from pynput import keyboard

gm_winx, gm_winy, gm_winw, gm_winh = None, None, None, None

def screen_shot(left=0, top=0, width=1920, height=1080):
        with mss.mss() as sct:
            screen = {
                'top': top,
                'left': left,
                'width': width,
                'height': height
            }
            sct_img = sct.grab(screen)
            return np.array(sct_img)
        
def calibrate_bot_win():
    window = screen_shot()
    gray = cv2.cvtColor(window, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 100000:
            x, y, w, h = cv2.boundingRect(contour)          
    return x, y, w, h

def on_press(key):
    global gm_winx, gm_winy, gm_winw, gm_winh

    try:
        if key.char == 's':
            gm_winx, gm_winy, gm_winw, gm_winh = calibrate_bot_win()
            print(f'Bot Window Calibrated: x: {gm_winx}, y: {gm_winy}, w: {gm_winw}, h: {gm_winh}')
            
            return False
        
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Press 's' on the menu page to calibrate the bot window.")
listener.join()

bot = TileBot(gm_winx, gm_winy, gm_winw, gm_winh)
bot.run()

