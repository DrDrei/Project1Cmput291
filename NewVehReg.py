'''
Created on Mar 10, 2016

@author: drei
'''

import tkinter as tk
import re as regex

class NewVehReg(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    isValid = False
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        widthText = 20
        heightText = 1
        
        label = tk.Label(self, text = 'Register a New Vehicle:')
        label.grid(row = 0, column = 0, columnspan = 2)
                
        serialLabel = tk.Label(self, text = 'Serial Number: ')
        serialLabel.grid(row = 1, column = 0)
        serialText = tk.Text(self, height = heightText, width = widthText)
        serialText.config(bg = self.valid)
        serialText.grid(row = 1, column = 1)
        serialConfig = '^\d{15}$'
          
        makerLabel = tk.Label(self, text = 'Vehicle Maker: ')
        makerLabel.grid(row = 2, column = 0)
        makerText = tk.Text(self, height = heightText, width = widthText)
        makerText.config(bg = self.valid)
        makerText.grid(row = 2, column = 1)
        makerConfig = '^[a-zA-Z0-9]{1,20}$'
          
        modelLabel = tk.Label(self, text = 'Model Number: ')
        modelLabel.grid(row = 3, column = 0)
        modelText = tk.Text(self, height = heightText, width = widthText)
        modelText.config(bg = self.valid)
        modelText.grid(row = 3, column = 1)
        modelConfig = '^[a-zA-Z0-9]{1,20}$'
         
          
        yearLabel = tk.Label(self, text = 'Year: ')
        yearLabel.grid(row = 4, column = 0)
        yearText = tk.Text(self, height = heightText, width = widthText)
        yearText.config(bg = self.valid)
        yearText.grid(row = 4, column = 1)
        yearConfig = '^\d{4}$'
          
          
        colorLabel = tk.Label(self, text = 'Color: ')
        colorLabel.grid(row = 5, column = 0)
        colorText = tk.Text(self, height = heightText, width = widthText)
        colorText.config(bg = self.valid)
        colorText.grid(row = 5, column = 1)
        colorConfig = '^[a-zA-Z]{1,10}$'
          
          
        typeLabel = tk.Label(self, text = 'Type_id: ')
        typeLabel.grid(row = 6, column = 0)
        typeText = tk.Text(self, height = heightText, width = widthText)
        typeText.config(bg = self.valid)
        typeText.grid(row = 6, column = 1)
        typeConfig = '^[1-9]\d*$'      
    
        submitBtn = tk.Button(self, text = 'Submit',
                            command = lambda: combineFuncs(validate(serialText, serialConfig),
                                                           validate(makerText, makerConfig),
                                                           validate(modelText, modelConfig),
                                                           validate(yearText, yearConfig),
                                                           validate(colorText, colorConfig),
                                                           validate(typeText, typeConfig)))
                                                                        
        submitBtn.grid(row = 7, column = 1)
        
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.grid(row = 7, column = 0)
        
        def validate(textField, regConfig):
            print(textField.get('1.0','end'))
            if regex.match(regConfig,textField.get('1.0','end')):
                textField.config(bg = self.valid)
                self.isValid = True
            else:
                textField.config(bg = self.invalid)
                self.isValid = False
                

        def combineFuncs(*funcs):
            def combinedFunc(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combinedFunc

