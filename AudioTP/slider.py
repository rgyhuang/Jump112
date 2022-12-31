import tkinter as tk
from tkinter import ttk
from cmu_112_graphics import *

class Slider():
    def __init__(self, screen, min_val, max_val, orientation):
        self.screen = screen
        self.start = min_val
        self.end = max_val
        self.orient = orientation
        #self.slider_setup()

    def slider_setup(self):

        self.screen.columnconfigure(0, weight=1)
        self.screen.columnconfigure(1, weight=3)
    
        self.currValue = tk.DoubleVar()
        slider_label = ttk.Label(self.screen, text='Slider:')
        slider_label.grid(
            column=0,
            row=0,
            sticky='w')  
        self.slider = ttk.Scale(
            self.screen, 
            from_=self.start,
            to=self.end,
            orient=self.orient,
            command=self.slider_changed,
            variable=self.currValue)
        self.slider.grid(
            column=1,
            row=0,
            sticky='we')

        # testing
        # current value label
        current_value_label = ttk.Label(
            self.screen,
            text='Current Value:'
        )

        current_value_label.grid(
            row=1,
            columnspan=2,
            sticky='n',
            ipadx=10,
            ipady=10
        )

        # value label
        self.value_label = ttk.Label(
            self.screen,
            text=self.get_current_value()
        )
        self.value_label.grid(
            row=2,
            columnspan=2,
            sticky='n'
        )

    def get_current_value(self):
        return '{: .2f}'.format(self.currValue.get())

    def slider_changed(self, event):
        self.value_label.configure(text=self.get_current_value())
    
    
# # # create slider
# root = tk.Tk()
# Slider(root, 0, 100,'horizontal')
