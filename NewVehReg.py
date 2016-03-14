'''
Created on Mar 10, 2016

@author: drei
'''

import tkinter as tk
import re as regex
from DBConnect import DBTables

class NewVehReg(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    isValid = False
    isDBValid = False
    connectionStr = ''
    vehicleData = []
        
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.connectionStr = connectionStr
        widthText = 20
        heightText = 1
        
        label = tk.Label(self, text = 'Register a New Vehicle:')
        label.grid(row = 0, column = 0, columnspan = 2)
        
        ownerLabel = tk.Label(self, text = 'Owner SIN: ')
        ownerLabel.grid(row = 1, column = 0)
        ownerText = tk.Text(self, height = heightText, width = widthText)
        ownerText.config(bg = self.valid)
        ownerText.grid(row = 1, column = 1)
        ownerConfig = '^[a-zA-Z0-9]{1,15}$'
                
        serialLabel = tk.Label(self, text = 'Serial Number: ')
        serialLabel.grid(row = 2, column = 0)
        serialText = tk.Text(self, height = heightText, width = widthText)
        serialText.config(bg = self.valid)
        serialText.grid(row = 2, column = 1)
        serialConfig = '^[a-zA-Z0-9]{1,15}$'
          
        makerLabel = tk.Label(self, text = 'Vehicle Maker: ')
        makerLabel.grid(row = 3, column = 0)
        makerText = tk.Text(self, height = heightText, width = widthText)
        makerText.config(bg = self.valid)
        makerText.grid(row = 3, column = 1)
        makerConfig = '^[a-zA-Z0-9]{1,20}$'
          
        modelLabel = tk.Label(self, text = 'Model Number: ')
        modelLabel.grid(row = 4, column = 0)
        modelText = tk.Text(self, height = heightText, width = widthText)
        modelText.config(bg = self.valid)
        modelText.grid(row = 4, column = 1)
        modelConfig = '^[a-zA-Z0-9]{1,20}$'
         
          
        yearLabel = tk.Label(self, text = 'Year: ')
        yearLabel.grid(row = 5, column = 0)
        yearText = tk.Text(self, height = heightText, width = widthText)
        yearText.config(bg = self.valid)
        yearText.grid(row = 5, column = 1)
        yearConfig = '^\d{4}$'
          
          
        colorLabel = tk.Label(self, text = 'Color: ')
        colorLabel.grid(row = 6, column = 0)
        colorText = tk.Text(self, height = heightText, width = widthText)
        colorText.config(bg = self.valid)
        colorText.grid(row = 6, column = 1)
        colorConfig = '^[a-zA-Z]{1,10}$'
          
          
        typeLabel = tk.Label(self, text = 'Type_id: ')
        typeLabel.grid(row = 7, column = 0)
        typeText = tk.Text(self, height = heightText, width = widthText)
        typeText.config(bg = self.valid)
        typeText.grid(row = 7, column = 1)
        typeConfig = '^[1-9]\d*$'      
            
        submitBtn = tk.Button(self, text = 'Submit',
                            command = lambda: combineFuncs(submit(),
                                                           validate(ownerText, ownerConfig),
                                                           validate(serialText, serialConfig),
                                                           validate(makerText, makerConfig),
                                                           validate(modelText, modelConfig),
                                                           validate(yearText, yearConfig),
                                                           validate(colorText, colorConfig),
                                                           validate(typeText, typeConfig),
                                                           validateDBserial(serialText),
                                                           validateDBtype(typeText),
                                                           validateDBowner(ownerText),
                                                           pushDataToDB()))
                                                                        
        submitBtn.grid(row = 8, column = 1)
        
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.grid(row = 8, column = 0)
        
        def submit():
            self.isValid = True
            self.isDBValid = True
            self.vehicleData = [serialText.get('1.0','end').rstrip(),
                                '\'' + makerText.get('1.0','end').rstrip()+'\'',
                                '\'' + modelText.get('1.0','end').rstrip() +'\'',
                                yearText.get('1.0','end').rstrip(),
                                '\'' + colorText.get('1.0','end').rstrip() +'\'',
                                typeText.get('1.0','end').rstrip()]
        
        def validate(textField, regConfig):
            print(textField.get('1.0','end'))
            if regex.match(regConfig,textField.get('1.0','end')):
                textField.config(bg = self.valid)
            else:
                textField.config(bg = self.invalid)
                self.isValid = False
                
        def validateDBowner(textField):
            if self.isValid:
                getOwner = 'SELECT sin FROM people'
                ownerData = DBTables.getData(self, self.connectionStr, getOwner)
                compStr = str(textField.get('1.0','end'))
                for each in ownerData:
                    print(str(each))
                    if str(each) == compStr:
                        self.isDBValid = False
                        textField.config(bg = self.invalid)
                        print('owner in DB')
                        
        def validateDBserial(textField):
            if self.isValid:
                getSerial = 'SELECT serial_no FROM vehicle'
                serialData = DBTables.getData(self, self.connectionStr, getSerial)
                compStr = textField.get('1.0','end')
                for each in serialData:
                    if int(each) == int(compStr):
                        self.isDBValid = False
                        textField.config(bg = self.invalid)
                        print('serial in DB')
        
        def validateDBtype(textField):
            if self.isValid:
                getType = 'SELECT type_id FROM vehicle_type'
                typeData = DBTables.getData(self, self.connectionStr, getType)
                intData = []
                for each in typeData:
                    intData.append(int(each))
                compStr = int(textField.get('1.0','end'))
                if compStr not in intData:
                    self.isDBValid = False
                    textField.config(bg = self.invalid)
                    print('type not in DB')
                    
                    
        def pushDataToDB():
            if self.isDBValid and self.isValid:
                insertStatement = 'INSERT INTO vehicle VALUES('
                for each in self.vehicleData:
                    insertStatement += each.rstrip() + ','
                insertStatement = insertStatement[:-1]
                insertStatement += ')'
                print(insertStatement)
                DBTables.pushData(self, self.connectionStr, insertStatement)
                
        def combineFuncs(*funcs):
            def combinedFunc(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combinedFunc

