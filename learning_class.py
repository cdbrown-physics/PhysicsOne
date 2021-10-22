import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
# import matplotlib.animation as animation
from matplotlib import style

import urllib.request
import json
import pandas as pd
import numpy as np

import datetime as dt
import time


style.use("ggplot")

LARGE_FONT=("Verdana", 12)

f = Figure(figsize=(9,5), dpi=70)
a = f.add_subplot(111)

global START_DATE_STRING
global END_DATE_STRING

class SeaofBTCapp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default='clienticon.ico')
        tk.Tk.wm_title(self, "Sea of BTC Client")
        
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, BTCe_Page,):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        # Normal Page Setup
        tk.Frame.__init__(self, parent)
        
        title = tk.Label(self, text='Graph Page', font=LARGE_FONT)
        
        home_button = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        
        plot_data_button=ttk.Button(self, text="Plot Data", command=lambda: self.PlotData())
        
        # Making a text box
        self.start_date_variable = tk.StringVar(self, value="Start date, if blank set to yeserday")
        start_date_textbox = tk.Entry(self, textvariabl=self.start_date_variable, width=30)
        start_text_label = tk.Label(self, text="Start date (YYYYMMDD)")
        
        self.end_date_variable = tk.StringVar(self, value="End date, if blank set to today")
        end_date_textbox = tk.Entry(self, textvariabl=self.end_date_variable, width=30)
        end_text_label = tk.Label(self, text="End date (YYYYMMDD)")
        
        # Actual Graph Part
        self.canvas=FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        
        
        title.pack(padx=10, pady=10)
        home_button.pack(side=tk.TOP)
        plot_data_button.pack(side=tk.TOP)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.RIGHT, expand=True)
        
        start_text_label.pack(side=tk.TOP, ipadx=0, ipady=0)
        start_date_textbox.pack(side=tk.TOP, padx=0, pady=0)
        end_text_label.pack(side=tk.TOP)
        end_date_textbox.pack(side=tk.TOP)
        
        # Trying to bind the plot button to the enter key
        # TODO: Find a way to find the 'Enter/Return' button to the update plots 
        # functionallity. I've tried a few things, but none of them appear to work. 
        
        
    def PlotData(self, event=None):
        global START_DATE_STRING
        global END_DATE_STRING
        
        #START_DATE_STRING = str(int(time.mktime(dt.datetime(2021, 1, 1).timetuple())))
        #END_DATE_STRING = str(int(time.mktime(dt.datetime(2021, 5, 26).timetuple())))
        START_DATE_STRING=self.start_date_variable.get()
        END_DATE_STRING=self.end_date_variable.get()
        
        if START_DATE_STRING=="Start date, if blank set to yeserday" or START_DATE_STRING=='':
            START_DATE_STRING = str(int(time.mktime((dt.datetime.today() - dt.timedelta(days=1)).timetuple())))
        elif len(START_DATE_STRING.strip())==8:
            START_DATE_STRING = str(int(time.mktime(dt.datetime(int(START_DATE_STRING[:4]), 
                                                                int(START_DATE_STRING[4:6]),
                                                                int(START_DATE_STRING[6:])).timetuple())))
        
        if END_DATE_STRING=="End date, if blank set to today" or END_DATE_STRING=='':
            END_DATE_STRING = str(int(time.mktime(dt.datetime.today().timetuple())))
        elif len(END_DATE_STRING.strip())==8:
            END_DATE_STRING = str(int(time.mktime(dt.datetime(int(END_DATE_STRING[:4]), 
                                                              int(END_DATE_STRING[4:6]),
                                                              int(END_DATE_STRING[6:])).timetuple())))
        dataLink = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={}&to={}".format(START_DATE_STRING, END_DATE_STRING)
        data = urllib.request.urlopen(dataLink)
        data = data.read().decode('utf-8')
        data = json.loads(data)
        data = pd.DataFrame(data)
        dates = [data['prices'][i][0] for i in range(len(data))]
        price = [data['prices'][i][1] for i in range(len(data))]
        
        a.clear()
        #print("Trying to make a plot?")
        #print(START_DATE_STRING, END_DATE_STRING)
        #print(price)
        # TODO: Convert the date into a human readable format
        a.plot(dates, price, c='C0', label='btc price')
        a.legend(loc=1)
        a.set_title("BTC pice in USD")
    
        a.set_xlabel("Date")
        a.set_ylabel("Price (USD)")
        
        self.canvas.draw()
            
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the start page, maybe some bitcoin stuff in here?", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
      
        
        agree_button = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_Page))
        disagree_button = ttk.Button(self, text="Disagree", command=quit )
        # graph_page_button = ttk.Button(self, text="Graph Page", command=lambda: controller.show_frame(GraphPage))
        
        agree_button.pack()
        disagree_button.pack()
        
            

def qf(quickPrint):
    print(quickPrint)

app = SeaofBTCapp()
app.mainloop()