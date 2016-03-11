'''
Created on Mar 10, 2016

@author: drei
'''

import tkinter as tk
from NewVehReg import NewVehReg
from AutoReg import AutoReg
from DLReg import DLReg
from VioReg import VioReg
from SearchEng import SearchEng

TITLE_FONT = ("Helvetica", 16, "bold")
class DBApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, NewVehReg, AutoReg, DLReg, VioReg, SearchEng):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Main Menu", font = TITLE_FONT)
        label.pack(fill='x', padx = 10, pady = 10)
        
        vehRegButton = tk.Button(self,
                                   text = "New Vehicle Registration",
                                   command = lambda: controller.show_frame('NewVehReg'))

        autoRegButton = tk.Button(self,
                                    text = "Auto Transaction",
                                    command = lambda: controller.show_frame('AutoReg'))

        DLRegButton = tk.Button(self,
                                text = "Driver License Registration",
                                command = lambda: controller.show_frame('DLReg'))        
        
        violationRecButton = tk.Button(self,
                                       text = "Violation Record",
                                         command = lambda: controller.show_frame('VioReg'))
        
        searchEngButton = tk.Button(self,
                                      text = "Search Engine",
                                      command = lambda: controller.show_frame('SearchEng'))        

        quitButton = tk.Button(self,
                             text = "Quit",
                             command = self.quit)
        
        vehRegButton.pack(fill = 'x')
        autoRegButton.pack(fill='x')
        DLRegButton.pack(fill='x')
        violationRecButton.pack(fill='x')
        searchEngButton.pack(fill='x')
        quitButton.pack(fill='x')


if __name__ == "__main__":
    app = DBApp()
    app.mainloop()