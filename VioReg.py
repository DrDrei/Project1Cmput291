'''
Created on Mar 10, 2016

@author: drei
'''
import tkinter as tk

class VioReg(tk.Frame):
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = 'Violation Record registration:')
        label.pack(fill = 'x')
        
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.pack()
