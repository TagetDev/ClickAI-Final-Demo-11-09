# Kütüphaneler
import threading
import pyautogui
import keyboard
from PIL import Image
from ultralytics import YOLO
import pydirectinput
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import csv


#flag & indexler
flag = True
flag1 = True
flag_hesap = False
flag_inst_one = True
flag_gonderme = False
i = 1


#Yorum Datası

def metinleri_cek(csv_dosya, ayirac=','):
    yazi_listesi = []
    with open(csv_dosya, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=ayirac)
        for row in reader:
            for metin in row:
                yazi_listesi.append(metin)
    return yazi_listesi

dosya_adi = 'metinler.csv'
yazi_listesi = metinleri_cek(dosya_adi)
rastgele_yazi = random.choice(yazi_listesi)

# f------------------------------------------------------Fonksiyon Alanları----------------------------------------------------------







#Tıklama İşlemleri

def hesap_degisikligi(i):
    positions = {
        2: 400,
        3: 500,
        4: 600,
        5: 700,
        6: 800,
        7: 880,
    }
    
    if i in positions:
        pyautogui.click(850, positions[i])
        
    
    
            






def run_bot(decision):
    global flag, flag1, rastgele_yazi, flag_hesap,flag_inst_one, flag_gonderme, i  # Bayrağın global olduğunu belirtin
    if "gurup_ikon_location" in decision:
        print(f"Clicking dm_gurup_icone at {decision['gurup_ikon_location']}")
        
        time.sleep(1)
        
        if flag:  # Eğer bayrak True ise işlemi gerçekleştir
            x, y = decision["gurup_ikon_location"]
            new_location = (x + 50, y)
            pyautogui.click(new_location)
            time.sleep(1.5)
            pyautogui.click(850, 750)
            flag = False  # İşlem tamamlandığında bayrağı False yapın
        
        
    elif "dm_ikon_location" in decision:
        print(f"Clicking dm_icon at {decision['dm_ikon_location']}")
        
        if flag1:  # Eğer bayrak True ise işlemi gerçekleştir
            pyautogui.click(decision["dm_ikon_location"])
            flag1 = False  # İşlem tamamlandığında bayrağı False yapın
       
    
    elif "insta_one_ikon_location" in decision:
        print(f"Clicking insta_one_icon at {decision['insta_one_ikon_location']}")
        if flag_inst_one:
            pyautogui.click(decision["insta_one_ikon_location"])
            time.sleep(1)
            flag_inst_one = False
    
            
    
    
    elif "yorum_ikonu_location" in decision:
        print(f"Clicking yorum_icon at {decision['yorum_ikonu_location']}")
        pyautogui.click(decision["yorum_ikonu_location"]) 
        time.sleep(2)
        pyautogui.write(f'{rastgele_yazi}')
        time.sleep(0.5)
        flag_hesap = True   
        flag_gonderme = True
    elif "gonderme_ikon_location" in decision:
        print(f"Clicking yor_gonderme_icon at {decision['gonderme_ikon_location']}")
        if flag_gonderme:
            pyautogui.click(decision["gonderme_ikon_location"])   
            time.sleep(3)
            flag_gonderme = False
        
        if flag_hesap:
            for _ in range(4):
                pyautogui.rightClick(850, 750)
                time.sleep(1.5)
            time.sleep(1.5)
            pyautogui.click(850, 50)
            time.sleep(1.5)
            i = i+1
            
            if i<8:
                hesap_degisikligi(i)
                
            else:
                print("HESAP BİTTİ") #uygulama degisikligi
                

            flag = True
            flag1 = True
            flag_hesap = False
            
        
        
    
      
        
#Konumların Alınması
def take_screenshot(stop_event, model):
    global flag_hesap  # Bu satırı ekleyin
    pyautogui.FAILSAFE = False

    while not stop_event.is_set():
        decision = {
            "gurup_ikon": False,
            "dm_ikon": False,
            "insta_one_ikon": False,
            "insta_two_ikon": False,
            "yapistir_ikon": False,
            "gonderme_ikon": False,
            "yorum_ikonu": False,
        }

        screenshot = pyautogui.screenshot()
        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())

        results = model([screenshot], conf=.20)  # return a list of Results objects
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = box
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            confidence = conf
            detected_class = cls
            name = names[int(cls)]

            if name == "gurup_ikon":
                decision["gurup_ikon"] = True
                decision["gurup_ikon_location"] = (center_x, center_y)

            elif name == "dm_ikon":
                decision["dm_ikon"] = True
                decision["dm_ikon_location"] = (center_x, center_y)

            
            elif name == "insta_one_ikon":
                decision["insta_one_ikon"] = True
                decision["insta_one_ikon_location"] = (center_x, center_y)

            elif name == "insta_two_ikon":
                decision["insta_two_ikon"] = True
                decision["insta_two_ikon_location"] = (center_x, center_y)

            elif name == "yapistir_ikon":
                decision["yapistir_ikon"] = True
                decision["yapistir_ikon_location"] = (center_x, center_y)

            elif name == "gonderme_ikon":
                decision["gonderme_ikon"] = True
                decision["gonderme_ikon_location"] = (center_x, center_y)

            elif name == "yorum_ikonu":
                decision["yorum_ikonu"] = True
                decision["yorum_ikonu_location"] = (center_x, center_y)
        
        run_bot(decision)


    
    
    
    
def main():
    print(pyautogui.KEYBOARD_KEYS)
    model = YOLO('best.pt')
    stop_event = threading.Event()
    
    screenshot_thread = threading.Thread(target=take_screenshot, args=(stop_event, model))
    screenshot_thread.start()

    keyboard.wait("q")

    stop_event.set()
    screenshot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()
