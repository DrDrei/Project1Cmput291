'''
Created on Mar 8, 2016

@author: drei
'''

from tkinter import *

class mainScreen:
    def __init__(self, parent):
        frame = Frame(parent)
        frame.pack()
        
        self.vehRegButton = Button(frame,
                                      text = "New Vehicle Registration", 
                                      fg = "black",
                                      command = lambda: self.vehReg())
        self.vehRegButton.pack(fill=X)

        self.autoRegButton = Button(frame,
                                      text = "Auto Transaction", 
                                      fg = "black",
                                      command = lambda: self.autoTrans())
        self.autoRegButton.pack(fill=X)

        self.DLRegButton = Button(frame,
                                      text = "Driver License Registration", 
                                      fg = "black",
                                      command = lambda: self.DLReg())        
        self.DLRegButton.pack(fill=X)


        self.violationRecButton = Button(frame,
                                      text = "Violation Record", 
                                      fg = "black",
                                      command = lambda: self.violationRec())
        
        self.violationRecButton.pack(fill=X)


        self.searchEngButton = Button(frame,
                                      text = "Search Engine", 
                                      fg = "black",
                                      command = lambda: self.searchEng())        
        self.searchEngButton.pack(fill=X)

        self.quitButton = Button(frame,
                             text = "Quit",
                             fg = "red",
                             command = lambda: frame.quit)
        self.quitButton.pack(fill=X)
        
    def vehReg(self):
        print("New Vehicle Registration Button pressed.")
        
    def autoTrans(self):
        print("Auto Transaction Button pressed.")
        
    def DLReg(self):
        print("Driver Lincense Registration Button pressed.")
        
    def violationRec(self):
        print("Violation Record Button pressed.")
        
    def searchEng(self):
        print("New Vehicle Registration Button pressed.")
        
    
if __name__ == "__main__":
    root = Tk()
    screen = mainScreen(root)
    root.mainloop()