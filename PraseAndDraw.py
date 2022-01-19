from datetime import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from statistics import mean
  
def Average(lst):
    return mean(lst)

def Percentile(model, ar):
    print(f"{model} 95%分位數 :", np.percentile(ar, 95))
    print(f"{model} 97%分位數 :", np.percentile(ar, 97))
    print(f"{model} 99%分位數 :", np.percentile(ar, 99))


class Work:
    def __init__(self):
        # Response time cost time
        self.response_time_bone, self.response_time_chest, self.response_time_ekg = [], [], []

        # Upload until output cost time
        self.response_time_bone2, self.response_time_chest2, self.response_time_ekg2  = [], [], []

        # Averge Line
        self.Averge_Bone, self.Average_Chest, self.Average_ekg = 0, 0, 0

    def calculate_time(self, data, model, mode):
        if mode == 'two_different':
            if model == 'Boneage':
                for i, n in enumerate(data['RT_Boneage']):
                    if (i+1) == len(data['RT_Boneage']):
                        break
                    else:
                        time_1 = datetime.strptime(data['RT_Boneage'][i],"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(data['RT_Boneage'][i+1],"%Y/%m/%d %H:%M:%S")
                        time_interval = time_2 - time_1
                        self.response_time_bone.append(int(time_interval.total_seconds()))
                return "OK"
              
            elif model == 'Chest':
                for i, n in enumerate(data['RT_Chest']):
                    # print('C', i)
                    if (i+1) == len(data['RT_Chest']):
                        break
                    else:
                        time_1 = datetime.strptime(data['RT_Chest'][i],"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(data['RT_Chest'][i+1],"%Y/%m/%d %H:%M:%S")
                        time_interval = time_2 - time_1
                        self.response_time_chest.append(int(time_interval.total_seconds()))
                return "OK"
              
            elif model == 'Ekg':
                for i, n in enumerate(data['RT_ekg']):
                    if (i+1) == len(data['RT_ekg']):
                        break
                    else:
                        time_1 = datetime.strptime(data['RT_Chest'][i],"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(data['RT_Chest'][i+1],"%Y/%m/%d %H:%M:%S")
                        time_interval = time_2 - time_1
                        self.response_time_ekg.append(int(time_interval.total_seconds()))
                return "OK"
              
        elif mode = 'in_util_out':
            if model == 'Boneage':
                for i, n in enumerate(data['RT_Boneage']):
                    if (i+1) == len(data['RT_Boneage']):
                        break
                    else:
                        time_1 = datetime.strptime(data['CT_BoneAge'][i],"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(data['RT_Boneage'][i],"%Y/%m/%d %H:%M:%S")
                        time_interval = time_2 - time_1
                        self.response_time_bone2.append(int(time_interval.total_seconds()))
                return "OK"
              
            elif model == 'Chest':
                for i, n in enumerate(data['RT_Chest']):
                    if (i+1) == len(data['RT_Chest']):
                        break
                    else:
                        time_1 = datetime.strptime(data['CT_Chest'][i],"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(data['RT_Chest'][i],"%Y/%m/%d %H:%M:%S")
                        time_interval = time_2 - time_1
                        self.response_time_chest2.append(int(time_interval.total_seconds()))
                return "OK"
              
            elif model == 'Ekg':
                for i, n in enumerate(data['RT_Ekg']):
                    if (i+1) == len(data['RT_Ekg']):
                        break
                    else:
                        time_1 = datetime.strptime(data['CT_Ekg'][i],"%Y/%m/%d %H:%M:%S")
                        time_2 = datetime.strptime(data['RT_Ekg'][i],"%Y/%m/%d %H:%M:%S")
                        time_interval = time_2 - time_1
                        self.response_time_ekg2.append(int(time_interval.total_seconds()))
                return "OK"



    def draw(self, data, model, response_list, mode):
        if mode == 'two_different':
            if model == 'Boneage':
                tick_spacing = data['RT_Boneage']
                tick_spacing = 15
                x = data['RT_Boneage'][1:]
                fig, ax = plt.subplots(1, 1)
                ax.plot(x, self.response_time_bone)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.title("Boneage Response Time", fontsize=20)
                plt.ylabel("time (s)")
                plt.xticks(fontsize=8, rotation=45)
                plt.xlabel("date")
                plt.tight_layout()
                plt.savefig('Response_Time_Bone.png', dpi=200)
                plt.show()

            elif model == 'Chest':
                tick_spacing = data['RT_Chest']
                tick_spacing = 55
                x = data['RT_Chest'][1:]
                fig, ax = plt.subplots(1, 1)
                ax.plot(x, self.response_time_chest)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.title("Chest Response Time", fontsize=20)
                plt.ylabel("time (s)")
                plt.xticks(fontsize=8, rotation=45)
                plt.xlabel("date")
                plt.tight_layout()
                plt.savefig('Response_Time_Chest.png', dpi=200)
                plt.show()

            elif model == 'Ekg':
                tick_spacing = data['RT_Ekg']
                tick_spacing = 55
                x = data['RT_Ekg'][1:]
                fig, ax = plt.subplots(1, 1)
                ax.plot(x, self.response_time_ekg)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.title("Chest Response Time", fontsize=20)
                plt.ylabel("time (s)")
                plt.xticks(fontsize=8, rotation=45)
                plt.xlabel("date")
                plt.tight_layout()
                plt.savefig('Response_Time_ekg.png', dpi=200)
                plt.show()


        elif mode = "in_util_out":
            if model == 'Boneage':
                tick_spacing = data['RT_Boneage']
                tick_spacing = 25
                x = data['RT_Boneage'][1:]
                fig, ax = plt.subplots(1, 1)
                ax.plot(x, self.response_time_bone2)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.title("Boneage Response Time(Since upload util output)", fontsize=16)
                plt.ylabel("time (s)")
                plt.xticks(fontsize=8, rotation=45)
                plt.xlabel("date")
                plt.tight_layout()
                plt.savefig('Response_Time_Bone_util_output.png', dpi=200)
                plt.show()
                
            elif model == 'Chest':
                tick_spacing = data['RT_Chest']
                tick_spacing = 72
                x = data['RT_Chest'][1:]
                fig, ax = plt.subplots(1, 1)
                ax.plot(x, self.response_time_chest2)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.title("Chest Response Time(Since Upload util output)", fontsize=16)
                plt.ylabel("time (s)")
                plt.xticks(fontsize=6, rotation=45)
                plt.xlabel("date")
                plt.tight_layout()
                plt.savefig('Response_Time_Chest_util_output.png', dpi=200)
                plt.show()
                
            elif model == 'Ekg':
                tick_spacing = data['RT_Ekg']
                tick_spacing = 72
                x = data['RT_Ekg'][1:]
                fig, ax = plt.subplots(1, 1)
                ax.plot(x, self.response_time_ekg2)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.title("Ecg Response Time(Since Upload util output)", fontsize=16)
                plt.ylabel("time (s)")
                plt.xticks(fontsize=6, rotation=45)
                plt.xlabel("date")
                plt.tight_layout()
                plt.savefig('Response_Time_ecg_util_output.png', dpi=200)
                plt.show()


    def main(self):
        with open('Log.txt', mode='r') as f:
            # Data
            data = eval(f.read())

            self.calculate_time(data, 'Boneage', 'in_to_out')
            self.calculate_time(data, 'Chest', 'in_util_out')
            self.calculate_time(data, 'Ekg', 'in_util_out')

            # Response Time
            print("Boneage averge time: ", Average(self.response_time_bone2))
            print("Chest average time: ", Average(self.response_time_chest2))
            print("ekg average time: ", Average(self.response_time_ekg2))


            # 95 97 99
            ar_bone = np.array(self.response_time_bone2)
            ar_chest = np.array(self.response_time_chest2)
            ar_ekg = np.array(self.response_time_ekg2)
            Percentile("Boneage", ar_bone)
            Percentile("Chest", ar_chest)
            Percentile("Ekg", ar_ekg)


            # Draw
            self.draw2(data, 'Boneage', self.response_time_bone2, self.Averge_Bone, 'in_util_out')
            self.draw2(data, 'Chest', self.response_time_chest2, self.Average_Chest, 'in_util_out')
            self.draw2(data, 'Ekg', self.response_time_ekg2, self.Average_Chest, 'in_util_out')
            f.close()
            print("End Draw")



if __name__ == '__main__':
    work = Work()
    work.main()
