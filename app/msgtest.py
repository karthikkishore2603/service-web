
import time 
from  pywhatkit import *
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()


msg="hello"
try:
    
    pywhatkit.sendwhatmsg_instantly(
        phone_no="+919487529436", 
        message=msg,
        tab_close=True
    )
    time.sleep(10)
    pyautogui.click()
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    print("Message sent!")
except Exception as e:
    print(str(e))