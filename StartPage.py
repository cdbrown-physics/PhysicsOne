# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 14:10:33 2021

@author: cody2
"""
import tkinter as tk

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the start page \n What kind of problem do you want to solve?", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        oneD_motion_button = ttk.Button(self, text="Projectile Motion", command=lambda: controller.show_frame(OneDMotionPage))
        oneD_motion_button.pack()