import cv2
import pyautogui
import keyboard
import time
import os
import threading

def take_screenshot(interval, stop_event):
    
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    while not stop_event.is_set():
 
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshots/screenshot_{timestamp}.png")

        stop_event.wait(interval)


def main():

    sure = int(input("kaç saniye bir SS alınacak süreyi giriniz lütfen: "))
    
    stop_event = threading.Event()
    
    ss_thread = threading.Thread(target=take_screenshot, args = (sure,stop_event))
    
    ss_thread.start()
    
    print("SS Almayı Durdurmak için 'q' tuşuna basabilirsiniz ")
    
    keyboard.wait("q")
    
    stop_event.set()
    
    ss_thread.join()
    
    print("Program Sonlandırıldı")
    
if __name__ == "__main__":
    
    main()
    
    
    
    
    