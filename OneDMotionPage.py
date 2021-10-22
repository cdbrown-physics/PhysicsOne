# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 14:03:45 2021

@author: cody2
"""
import tkinter as tk
from tkinter import ttk

from PhysicsOneApp import StartPage

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
# import matplotlib.animation as animation
from matplotlib import style

from physics_solver import one_dimention_solver
import numpy as np

class OneDMotionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Setting up the eventual plot
        self.fig = Figure(figsize=(8,5), dpi=100)
        self.graph = self.fig.add_subplot(111)
        row_count = 0
        col_count = 0
        
        label = tk.Label(self, text='Use this page to solve your one dimentional motion problems', font=16)
        label.grid(row=0, column=1)
        
        solve_button = tk.Button(self, text="Solve", bg='green', height=5, width=15, command=lambda: self.SolveButton())
        solve_button.grid(row=0, column=2, rowspan=3)
        
        clear_button = tk.Button(self, text='Clear', width=15, command=lambda: self.ClearButton())
        clear_button.grid(row=3, column=2, rowspan=2)
        
        home_button = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        home_button.grid(row=row_count, column=col_count)
        row_count += 1
        
        
        # Setting up all the text entried for the inputs
        self.x0_variable = tk.StringVar(self, value='10')
        self.x0_textbox = tk.Entry(self, textvariabl=self.x0_variable, width=10)
        x0_label = tk.Label(self, text="Initial Position")
        x0_label.grid(row=row_count, column=col_count)
        row_count += 1
        self.x0_textbox.grid(row=row_count, column=col_count)
        row_count += 1
        
        self.xf_variable = tk.StringVar(self, value='15')
        self.xf_textbox = tk.Entry(self, textvariabl=self.xf_variable, width=10)
        xf_label = tk.Label(self, text="Final Position")
        xf_label.grid(row=row_count, column=col_count)
        row_count += 1
        self.xf_textbox.grid(row=row_count, column=col_count)
        row_count += 1
        
        self.v0_variable = tk.StringVar(self, value='1')
        self.v0_textbox = tk.Entry(self, textvariabl=self.v0_variable, width=10)
        v0_label = tk.Label(self, text="Initial Velocity")
        v0_label.grid(row=row_count, column=col_count)
        row_count += 1
        self.v0_textbox.grid(row=row_count, column=col_count)
        row_count += 1
        
        self.vf_variable = tk.StringVar(self)
        self.vf_textbox = tk.Entry(self, textvariabl=self.vf_variable, width=10)
        vf_label = tk.Label(self, text="Final Velocity")
        vf_label.grid(row=row_count, column=col_count)
        row_count += 1
        self.vf_textbox.grid(row=row_count, column=col_count)
        row_count+=1
        
        self.a_variable = tk.StringVar(self, value='0')
        self.a_textbox = tk.Entry(self, textvariabl=self.a_variable, width=10)
        a_label = tk.Label(self, text="Acceleration")
        a_label.grid(row=row_count, column=col_count)
        row_count += 1
        self.a_textbox.grid(row=row_count, column=col_count)
        row_count += 1
        
        self.t_variable = tk.StringVar(self)
        self.t_textbox = tk.Entry(self, textvariabl=self.t_variable, width=10)
        t_label = tk.Label(self, text="Time")
        t_label.grid(row=row_count, column=col_count)
        row_count += 1
        self.t_textbox.grid(row=row_count, column=col_count)
        row_count = 1
        col_count += 1
        
        # Actual Graph Part
        self.canvas=FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=row_count, column=col_count, rowspan=20)
        
    def SolveButton(self):
        # Make a list of the variables we have
        if self.x0_variable.get() == '':
            x0 = None
        else:
            x0 = float(self.x0_variable.get())
            
        if self.xf_variable.get() == '':
            xf = None
        else:
            xf = float(self.xf_variable.get())
            
        if self.v0_variable.get() == '':
            v0 = None
        else:
            v0 = float(self.v0_variable.get())
            
        if self.vf_variable.get() == '':
            vf = None
        else:
            vf = float(self.vf_variable.get())
            
        if self.a_variable.get() == '':
            a = None
        else:
            a = float(self.a_variable.get())
            
        if self.t_variable.get() == '':
            t = None
        else:
            t = float(self.t_variable.get())
            
        variables = {'x0':x0, 'xf':xf, 'v0':v0, 'vf':vf, 'a':a, 't':t}
        variables = one_dimention_solver(x0=x0, xf=xf, v0=v0, vf=vf, a=a, t=t)
        
        # Update all the values on the screen now that we have a solution.
        self.x0_variable.set(str(variables['x0']))
        self.xf_variable.set(str(variables['xf']))
        self.v0_variable.set(str(variables['v0']))
        self.vf_variable.set(str(variables['vf']))
        self.a_variable.set(str(variables['a']))
        self.t_variable.set(str(variables['t']))
        
        self.x0_textbox.delete(0, 'end')
        self.xf_textbox.delete(0, 'end')
        self.v0_textbox.delete(0, 'end')
        self.vf_textbox.delete(0, 'end')
        self.a_textbox.delete(0, 'end')
        self.t_textbox.delete(0, 'end')
        
        self.x0_textbox.insert(0,'{0:.2f}'.format(variables['x0']))
        self.xf_textbox.insert(0, '{0:.2f}'.format(variables['xf']))
        self.v0_textbox.insert(0, '{0:.2f}'.format(variables['v0']))
        self.vf_textbox.insert(0, '{0:.2f}'.format(variables['vf']))
        self.a_textbox.insert(0, '{0:.2f}'.format(variables['a']))
        self.t_textbox.insert(0, '{0:.2f}'.format(variables['t']))
        
        # Update the plot with what ever values we just solved for
        position_data = lambda t : variables['x0'] + variables['v0']*t + 0.5*variables['a']*t**2
        time_data = np.arange(0, variables['t'], abs(variables['t']/100) )
        
        self.graph.clear()
        self.graph.plot(time_data, position_data(time_data),)
        #self.a.legend(loc=1)
        self.graph.set_title("Position vs Time in One Dimention")
    
        self.graph.set_xlabel("Time")
        self.graph.set_ylabel("Position")
        
        self.canvas.draw()
        
        return None
        
    def ClearButton(self):
        """
        Function that clearns all the text boxes

        Returns
        -------
        None.

        """
        self.x0_variable=''
        self.xf_variable=''
        self.v0_variable=''
        self.vf_variable=''
        self.a_variable=''
        self.t_variable=''
        
        self.x0_textbox.delete(0, 'end')
        self.xf_textbox.delete(0, 'end')
        self.v0_textbox.delete(0, 'end')
        self.vf_textbox.delete(0, 'end')
        self.a_textbox.delete(0, 'end')
        self.t_textbox.delete(0, 'end')
        
        self.x0_textbox.insert(0, self.x0_variable)
        self.xf_textbox.insert(0, self.xf_variable)
        self.v0_textbox.insert(0, self.v0_variable)
        self.vf_textbox.insert(0, self.vf_variable)
        self.a_textbox.insert(0, self.a_variable)
        self.t_textbox.insert(0, self.t_variable)
        
        self.graph.clear()

        self.canvas.draw()
        
        return None