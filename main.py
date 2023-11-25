import tkinter as tk
import urllib.request
from proxy_setting import set_proxy_settings, disable_proxy_settings
from mitmproxy_fetch import threadstart
from key_gen import creatCA
import threading
import os
import requests
import json
import sys
import csv

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class URLMeter():
    def __init__(self) -> None:
        super().__init__()
        self.url = None

    def update(self, urlstr):
        self.url = urlstr

class proxyEnableButton(tk.Button):
    def __init__(self) -> None:
        super().__init__()

        self["text"]    = 'Enable Proxy'
        self["command"] = lambda: set_proxy_settings("127.0.0.1", 8080)

class proxyDisableButton(tk.Button):
    def __init__(self) -> None:
        super().__init__()

        self["text"]    = 'Disable Proxy'
        self["command"] = disable_proxy_settings

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        creatCA()

        self.url = None
        self.title('Reverse1999 Export')
        self.geometry('800x600')
        self.resizable(False,False)
        self.protocol('WM_DELETE_WINDOW', self.close)


        if getattr(sys, 'frozen', False):
            self.application_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

        elif __file__:
            self.application_path = os.path.dirname(__file__)

        # if os.path.isfile("summonURL.txt"):
        #     os.remove("summonURL.txt")

        self.button1 = proxyEnableButton()
        self.button1.place(x=20,y=20)

        self.button2 = proxyDisableButton()
        self.button2.place(x=120,y=20)

        self.button3 = tk.Button(text="Search summon url", command=self.startFetching)
        self.button3.place(x=20,y=60)

        self.button4 = tk.Button(text="Export", command=self.export)
        self.button4.place(x=20,y=100)

        self.label1 = tk.Label(self, text="Proxy close.", font=20)
        self.label1.place(x=400,y=20)
        self.set_label1()

        self.label2 = tk.Label(self, text="", font=20)
        self.label2.place(x=400,y=60)
        self.set_label2()

        
    def set_label1(self):
        if urllib.request.getproxies():
            self.label1['text'] = "Proxy enable."
        else:
            self.label1['text'] = "Proxy disable."
        self.after(100, self.set_label1)

    def set_label2(self):
        if os.path.isfile("summonURL.txt"):
            self.label2['text'] = "Finish Fetching"
        self.after(100, self.set_label2)

    def startFetching(self):
        thread = threading.Thread(target=threadstart)
        thread.daemon = True
        thread.start()

    def export(self):
        disable_proxy_settings()
        csvfile = open('allsummon.csv', 'w', newline='')
        writer = csv.writer(csvfile)
        
        if os.path.isfile("summonURL.txt"):
            f_ = open("summonURL.txt")
            summonURL = f_.read()

            res = requests.get(summonURL)
            res = res.json()

            conf_ = open(os.path.join(self.application_path, "config.json"),encoding="utf-8")
            conf = json.load(conf_)

            confall_ = open(os.path.join(self.application_path, "configAll.json"),encoding="utf-8")
            confall = json.load(confall_)
            print(confall)

            resultList = []
            for item in reversed(res['data']['pageData']):

                if item['poolType']==3 :
                    resultList.extend(item['gainIds'])


            count=0
            countSIX=0
            summonf = open("summonLOG.txt",'w')
            for i in resultList:
                print([k for k,v in confall.items() if v == str(i)][0])
                writer.writerow([[k for k,v in confall.items() if v == str(i)][0], str(i)])

                count+=1
                if i in conf.values():
                    summonf.write([k for k,v in conf.items() if v == i][0])
                    summonf.write(str(count))
                    summonf.write("\n")
                    count=0
                    countSIX+=1
            csvfile.close()

            pieList = [countSIX, len(resultList)-countSIX]

            fig = Figure(figsize = (5, 5), dpi = 100)
            canvas = FigureCanvasTkAgg(fig,master = self)
            canvas.draw()

            axes = fig.add_subplot()
            axes.pie(pieList,
                    radius=1.5,
                    labels=['Six star',''],
                    autopct='%.1f%%')

            canvas.get_tk_widget().pack(side=tk.BOTTOM, expand=0)

    def close(self):
        disable_proxy_settings()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    # pyinstaller -w --onefile --add-data "config.json;." main.py
    # pyinstaller -w --onefile --add-data "config.json;." --add-data "configAll.json;." main.py
