
import tkinter as tk
import time

from NewVehReg import NewVehReg
from AutoReg import AutoReg
from DLReg import DLReg
from VioReg import VioReg
from SearchEng import SearchEng
from NewPerson import NewPerson
from NewPerson2 import NewPerson2
from NewPerson3 import NewPerson3
from DBConnect import DBTables

class DBApp(tk.Tk):
    def __init__(self, connectionStr, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, NewVehReg, AutoReg, DLReg, VioReg, SearchEng, NewPerson, NewPerson2, NewPerson3):
            page_name = F.__name__
            frame = F(connectionStr, container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Main Menu", font = ("Helvetica", 16, "bold"))
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
    initDB = DBTables()
    initDB.CreateTables()
    while not initDB.connectionStr:
        time.sleep(3)
        print(initDB.connectionStr)
    app = DBApp(initDB.connectionStr)
    app.mainloop()
    