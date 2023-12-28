import cv2
import numpy as np
import mss
import os
import pyautogui

class TileBot:
    def __init__(self, x, y, w, h):
        path = os.path.dirname(os.path.dirname(__file__))
        self.img_path = os.path.join(path, 'img')
        self.x, self.y, self.w, self.h = x, y, w, h

    def screen_shot(self):
        with mss.mss() as sct:
            screen = {
                'left': self.x,
                'top': self.y,
                'width': self.w,
                'height': self.h
            }
            sct_img = sct.grab(screen)
            return np.array(sct_img)

        
    def get_gm_win_dim(self):
         return self.x, self.y, self.w, self.h
        
    def run(self):
        while True:
            layout_img = self.screen_shot()
            img_quality_cf = 4  # This is a value that divides the image dimensions/quality. Higher value means faster but less accurate temp matching.
                                # This should be sufficient for 1920x1080 resolution. 
            layout_img = cv2.resize(layout_img, (0,0), fx=1/img_quality_cf, fy=1/img_quality_cf)
            tile_img = cv2.imread(os.path.join(self.img_path, 'tile.png'), cv2.IMREAD_UNCHANGED)
            tile_img = cv2.resize(tile_img, (0,0), fx=self.w/623/img_quality_cf, fy=self.h/933/img_quality_cf)
            tile_img = tile_img[0:tile_img.shape[0]//2, 0:]

            result = cv2.matchTemplate(layout_img, tile_img, cv2.TM_CCOEFF_NORMED)

            w = tile_img.shape[1]
            h = tile_img.shape[0]

            threshold = 0.8

            yloc, xloc = np.where(result >= threshold)

            rects = []
            for (x, y) in zip(xloc, yloc):
                rects.append([int(x), int(y), int(w), int(h)])
                rects.append([int(x), int(y), int(w), int(h)])

            rects, _ = cv2.groupRectangles(rects, 1, 0.2)

            if len(rects) == 0:
                print('No tiles detected')
            else:
                print(rects)

            for (x, y, w, h) in rects:
                cv2.rectangle(layout_img, (x,y), (x + w, y + h), (0, 255, 255), 2)
                pyautogui.click(self.x + x*img_quality_cf + w*img_quality_cf/2, self.y + y*img_quality_cf + h*img_quality_cf/2)

            cv2.imshow('TileBot', layout_img)
            cv2.setWindowProperty("TileBot", cv2.WND_PROP_TOPMOST, 1)

            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()