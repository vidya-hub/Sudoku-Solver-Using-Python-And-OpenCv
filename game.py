import os
import win32gui
import win32ui
import win32con
import numpy as np
import cv2
import win32com.client
import win32gui
import win32process
import time

# properties
w = 0
h = 0
hwnd = None
cropped_x = 0
cropped_y = 0
offset_x = 0
offset_y = 0
hwnd = win32gui.GetForegroundWindow()

_, pid = win32process.GetWindowThreadProcessId(hwnd)

shell = win32com.client.Dispatch("WScript.Shell")




def windowCapture():
# set this
    # bmpfilenamename = "out.bmp" #set this
    hwnd = win32gui.FindWindow(None, "Microsoft Sudoku")
    # hwnd=None
    if not hwnd:
            raise Exception('Window not found: {}'.format("Microsoft Sudoku"))
    print(hwnd)
    wDC = win32gui.GetWindowDC(hwnd)
            # get the window size
    window_rect = win32gui.GetWindowRect(hwnd)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]

    # account for the window border and titlebar and cut them off
    border_pixels = 8
    titlebar_pixels = 30
    w = w - (border_pixels * 2)
    h = h - titlebar_pixels - border_pixels
    cropped_x = border_pixels
    cropped_y = titlebar_pixels

    # set the cropped coordinates offset so we can translate screenshot
    # images into actual screen positions
    offset_x = window_rect[0] + cropped_x
    offset_y = window_rect[1] + cropped_y
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)

    # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)
    img = img[...,:3]
    img = np.ascontiguousarray(img) 
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return img

os.system("explorer.exe shell:appsFolder\Microsoft.MicrosoftSudoku_8wekyb3d8bbwe!App")

time.sleep(5)

while True:
    capture = windowCapture()
    cv2.imshow(
    "OK it's Over See the Result",
     capture,
     )
    
    if cv2.waitKey(1) == 27:
        # os.system("taskkill /f /im  shell:appsFolder\Microsoft.MicrosoftSudoku_8wekyb3d8bbwe!App")
        break

cv2.destroyAllWindows()

# print(windowCapture())