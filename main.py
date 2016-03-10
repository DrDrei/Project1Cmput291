'''
Created on Mar 10, 2016

@author: drei
'''

import tkinter as tk
from pip._vendor.cachecontrol import controller

TITLE_FONT = ("Helvetica", 16, "bold")

class DBApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, MainMenu, NewVehReg):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

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
                                    text = "Auto Transaction")

        DLRegButton = tk.Button(self,
                                text = "Driver License Registration")        
        
        violationRecButton = tk.Button(self,
                                         text = "Violation Record")
        
        searchEngButton = tk.Button(self,
                                      text = "Search Engine")        

        quitButton = tk.Button(self,
                             text = "Quit",
                             command = self.quit)
        
        vehRegButton.pack(fill = 'x')
        autoRegButton.pack(fill='x')
        DLRegButton.pack(fill='x')
        violationRecButton.pack(fill='x')
        searchEngButton.pack(fill='x')
        quitButton.pack(fill='x')
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Go to Main Menu",
                            command=lambda: controller.show_frame("MainMenu"))
        button1.pack()
        button2.pack()
        button3.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
class NewVehReg(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = 'Register a New Vehicle')
        label.pack(fill = 'x')
        
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.pack()

if __name__ == "__main__":
    app = DBApp()
    app.mainloop()