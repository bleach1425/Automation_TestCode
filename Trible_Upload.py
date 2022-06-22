import time
import requests
import os
import gc
import threading
import shutil
import random

import xml.etree.ElementTree as ET
from functools import wraps
from pydicom import dcmread
from pydicom.data import get_testdata_files
from datetime import datetime


# Boneage 3
# Cxr 2

def main_work_print(coder):
    # 第二層回傳帶入func
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            print(f"Coder: {coder}")
            print('')
            print('-' * 10)
            print("Check time: ", datetime.now())
            func(*args, **kwargs)
            print('-' * 10)
            print('')
            return "OK"
        return inner_wrapper
    return wrapper


class Dicom_fix:
    def __init__(self):
        pass

    def fix(self, filename, id, new_file):
        print("*" * 9)
        print("Fix: ", filename, id, new_file)
        print("*" * 9)
        ds = dcmread(filename)
        ds.PatientID = id
        ds.save_as(new_file)
        while not os.path.isfile(new_file):
            time.sleep(1)

    def check(self):
        ds = dcmread('ram.dcm')
        print(ds.PatientID)


def ekg_fix(filename, id, new_file):
    print("*" * 9)
    print("Fix: ", filename, id, new_file)
    print("*" * 9)
    tree = ET.parse(filename)
    root = tree.getroot()
    for _ in root.iter("PatientID"):
        _.text = id
    tree.write(new_file)




class Work(Dicom_fix):
    def __init__(self):
        self.url = "http://192.168.5.122/query"
        self.pid_title = "offcial_2"

        # Path
        try:
            self.Bone_path = os.listdir("./data/Boneage")
            self.Chest_path = os.listdir("./data/Chest")
            self.Ekg_path = os.listdir("./data/Ekg")
        except:
            raise FileNotFoundError("Please Check your `./data/<model>`")
            

        # Target Upload Num
        self.bone_target_num = 240
        self.chest_target_num = 720
        self.ekg_target_num = 720

        # Vali
        self.boneage_num = 0
        self.chest_num = 0
        self.ekg_num = 0

        # Id
        self.bone_id = 1
        self.chest_id = 1
        self.ekg_id = 1

        # Set init num
        r_bone = requests.post(self.url, json={"modelOpt": "boneage"})
        r_chest = requests.post(self.url, json={"modelOpt": "cxr_detection"})
        r_ekg = requests.post(self.url, json={"modelOpt": "ekg"})

        self.upload_boneage = len(eval(r_bone.text))
        self.upload_chest = len(eval(r_chest.text))
        self.upload_ekg = len(eval(r_ekg.text))

        # Plot Dict
        self.result = {
            "CT_Chest": [],
            "CT_BoneAge": [],
            "RT_Chest": [],
            "RT_Boneage": [],
            "CT_Ekg": [],
            "RT_Ekg": []
        }

        # Waitting time
        self.bone_wait, self.chest_wait, self.ekg_wait = 360, 120, 120

    def upload_work(self, model):
        if model == 'boneage':
            while True:
                if self.boneage_num == self.bone_target_num:
                    break
                target = random.choice(self.Bone_path)
                super().fix("./data/Boneage/" + target, self.pid_title + f"_{self.bone_id}", f'RAM_Boneage_{self.bone_id}.dcm')
                try:
                    shutil.move(f'RAM_Boneage_{self.bone_id}.dcm', '/secure/imgs/boneage')
                except:
                    while not os.path.isfile(f"RAM_Chest_{self.bone_id}.dcm"):
                        time.sleep(2)
                    shutil.move(f'RAM_Chest_{self.bone_id}.dcm', '/secure/imgs/boneage')
                # ------------------------------------------------- #
                self.result['CT_BoneAge'].append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
                self.boneage_num += 1
                self.bone_id += 1
                # ------------------------------------------------- #
                print(f"上傳了{str(self.boneage_num)}個BONEAGE檔案")
                gc.collect()
                time.sleep(self.bone_wait)
        elif model == 'chest':
            while True:
                if self.chest_num == self.chest_target_num:
                    break
                target = random.choice(self.Chest_path)
                # filename, id, new_file_name
                super().fix("./data/Chest/" + target, self.pid_title + f'_{self.chest_id}', f'RAM_Chest_{self.chest_id}.dcm')
                try:
                    shutil.move(f'RAM_Chest_{self.chest_id}.dcm', '/secure/imgs/cxr_detection')
                except:
                    print("Error")
                    while not os.path.isfile(f"RAM_Chest_{self.chest_id}.dcm"):
                        time.sleep(2)
                    shutil.move(f'RAM_Chest_{self.chest_id}.dcm', '/secure/imgs/cxr_detection')
                # ------------------------------------------------- #
                self.result['CT_Chest'].append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
                self.chest_num += 1
                self.chest_id += 1
                # ------------------------------------------------- #
                print(f"上傳了{str(self.chest_num)}個CHEST檔案")
                gc.collect()
                time.sleep(self.chest_wait)
        elif model == 'ekg':            
            while True:
                if self.ekg_num == self.ekg_target_num:
                    break
                target = random.choice(self.Ekg_path)
                # filename, id, new_file_name 
                ekg_fix("./data/Ekg/" + target, self.pid_title + f'_{self.ekg_id}', f'RAM_Ekg_{self.ekg_id}.xml')
                try:
                    print("From path: ", os.getcwd())
                    print("move: ", f"RAM_Ekg_{self.ekg_id}.xml")
                    shutil.move(f'RAM_Ekg_{self.ekg_id}.xml' + target, '/secure/imgs/ekg')
                except:
                    print("Error")
                    while not os.path.isfile(f"RAM_Ekg_{self.ekg_id}.xml"):
                        time.sleep(2)
                    shutil.move(f'RAM_Ekg_{self.ekg_id}.xml', '/secure/imgs/ekg')
                # ------------------------------------------------- #
                self.result['CT_Ekg'].append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
                self.ekg_num += 1
                self.ekg_id += 1
                # ------------------------------------------------- #
                print(f"上傳了{str(self.ekg_num)}個Ekg檔案")
                gc.collect()
                time.sleep(self.ekg_wait)
            

    @main_work_print("John")
    def main_work(self, model):
        if model == 'boneage':
            print("Check model: ",  model)
            r = requests.post(self.url, json={"modelOpt": f"{model}"})
            if len(eval(r.text)) != self.upload_boneage:
                add_num = len(eval(r.text)) - self.upload_boneage
                self.upload_boneage = len(eval(r.text))
                [self.result['RT_Boneage'].append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))) for n in range(add_num)]
            print("Response code: ", r.status_code)
            print("Inference num: ", len(eval(r.text)))
            gc.collect()

        elif model == 'cxr_detection':
            print("Check model: ",  model)
            r = requests.post(self.url, json={"modelOpt": f"{model}"})
            if len(eval(r.text)) != self.upload_chest:
                add_num = len(eval(r.text)) - self.upload_chest
                self.upload_chest = len(eval(r.text))
                [self.result['RT_Chest'].append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))) for n in range(add_num)]
            print("Response code: ", r.status_code)
            print("Inference num: ", len(eval(r.text)))
            gc.collect()

        elif model == 'ekg':
            print("Check model: ",  model)
            r = requests.post(self.url, json={"modelOpt": f"{model}"})
            if len(eval(r.text)) != self.upload_ekg:
                add_num = len(eval(r.text)) - self.upload_ekg
                self.upload_ekg = len(eval(r.text))
                [self.result['RT_Ekg'].append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))) for n in range(add_num)]
            print("Response code: ", r.status_code)
            print("Inference num: ", len(eval(r.text)))
            gc.collect()

    def main(self):
        # Child work
        t1 = threading.Thread(target = self.upload_work, args= ('boneage',))
        t2 = threading.Thread(target = self.upload_work, args= ('chest',))
        t3 = threading.Thread(target = self.upload_work, args= ('ekg',))

        # Driver
        t1.start()
        t2.start()
        t3.start()

        # Main 每1秒確認結果
        while True:
            with open('./Log.txt', mode='w', encoding='utf-8') as f:
                f.write(str(self.result))
                f.close()
                print("中斷條件1: ", self.boneage_num, self.chest_num, self.ekg_num)
                if self.boneage_num == self.bone_target_num and self.chest_num == self.chest_target_num and self.ekg_num == self.ekg_target_num:
                    print('')
                    print('-' * 10)
                    print("Upload Done.")
                    print('-' * 10)
                    print("檢查一下Dict: ", self.result)
                    # Final Step 每1秒確認是否self.result數量及inference完畢
                    while True:
                        print("**** Final: Result Dict Check  ****")
                        print("Result Boneage 確認數量: ", len(self.result['CT_BoneAge']), len(self.result['RT_Boneage']))
                        print("Result Chest 確認數量: ", len(self.result['CT_Chest']), len(self.result['RT_Chest']))
                        print("Result Ekg 確認數量: ", len(self.result['CT_Ekg']), len(self.result['RT_Ekg']))
                        self.main_work(model='boneage')
                        self.main_work(model='cxr_detection')
                        self.main_work(model='ekg')

                        with open("./Log.txt", mode='w', encoding='utf-8') as f:
                            f.write(str(self.result))
                            f.close()
                            if len(self.result['CT_Chest']) == len(self.result['RT_Chest']) and len(self.result['CT_BoneAge']) == len(self.result['RT_Boneage']) and len(self.result['CT_Ekg']) == len(self.result['RT_Ekg']):
                                with open("./Log.txt", mode='w', encoding='utf-8') as f:
                                    f.write(str(self.result))
                                    print("Result Table: ", self.result)
                                    f.close()
                                    break
                        time.sleep(1)
                        gc.collect()
                    break
                self.main_work(model='boneage') 
                self.main_work(model='cxr_detection')
                self.main_work(model='ekg')
                gc.collect()
                time.sleep(1)


if __name__ == '__main__':
    work = Work()
    work.main()
    print('Test End.')
