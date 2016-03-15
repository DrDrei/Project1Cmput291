

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
        rowIndex = 0
        
        
        label = tk.Label(self, text = 'Register a new Person:')
        label.grid(row = rowIndex, column = 0, columnspan = 2)
        
        rowIndex += 1
        ownerLabel = tk.Label(self, text = 'Primary Owner SIN: ')
        ownerLabel.grid(row = rowIndex, column = 0)
        ownerText = tk.Text(self, height = heightText, width = widthText)
        ownerText.config(bg = self.valid)
        ownerText.grid(row = rowIndex, column = 1)
        ownerConfig = '^[a-zA-Z0-9]{1,15}$'

        rowIndex += 1        
        ownerLabelErr = tk.Label(self, text = 'Primary Owner not in Database, please add them.')
        ownerLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        ownerLabelErr.grid_remove()
        
        rowIndex += 1
        secondaryLabel = tk.Label(self, text = 'Secondary Owner SIN: ')
        secondaryLabel.grid(row = rowIndex, column = 0)
        secondaryText = tk.Text(self, height = heightText, width = widthText)
        secondaryText.config(bg = self.valid)
        secondaryText.grid(row = rowIndex, column = 1)
        secondaryConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        secondaryLabelErr = tk.Label(self, text = 'Secondary Owner not in Database, please add them.')
        secondaryLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        secondaryLabelErr.grid_remove()
        
        rowIndex += 1       
        serialLabel = tk.Label(self, text = 'Serial Number: ')
        serialLabel.grid(row = rowIndex, column = 0)
        serialText = tk.Text(self, height = heightText, width = widthText)
        serialText.config(bg = self.valid)
        serialText.grid(row = rowIndex, column = 1)
        serialConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        serialLabelErr = tk.Label(self, text = 'Invalid Serial Number Input')
        serialLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        serialLabelErr.grid_remove()
         
        rowIndex += 1  
        makerLabel = tk.Label(self, text = 'Vehicle Maker: ')
        makerLabel.grid(row = rowIndex, column = 0)
        makerText = tk.Text(self, height = heightText, width = widthText)
        makerText.config(bg = self.valid)
        makerText.grid(row = rowIndex, column = 1)
        makerConfig = '^[a-zA-Z0-9]{1,20}$'
        
        
        rowIndex += 1
        makerLabelErr = tk.Label(self, text = 'Invalid Vehicle Maker Input')
        makerLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        makerLabelErr.grid_remove()
         
        rowIndex += 1  
        modelLabel = tk.Label(self, text = 'Model Number: ')
        modelLabel.grid(row = rowIndex, column = 0)
        modelText = tk.Text(self, height = heightText, width = widthText)
        modelText.config(bg = self.valid)
        modelText.grid(row = rowIndex, column = 1)
        modelConfig = '^[a-zA-Z0-9]{1,20}$'
         
        rowIndex += 1
        modelLabelErr = tk.Label(self, text = 'Invalid Model Number Input')
        modelLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        modelLabelErr.grid_remove()
         
        rowIndex += 1  
        yearLabel = tk.Label(self, text = 'Year: ')
        yearLabel.grid(row = rowIndex, column = 0)
        yearText = tk.Text(self, height = heightText, width = widthText)
        yearText.config(bg = self.valid)
        yearText.grid(row = rowIndex, column = 1)
        yearConfig = '^\d{4}$'
        
        rowIndex += 1
        yearLabelErr = tk.Label(self, text = 'Invalid Year Input')
        yearLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        yearLabelErr.grid_remove()  
         
        rowIndex += 1  
        colorLabel = tk.Label(self, text = 'Color: ')
        colorLabel.grid(row = rowIndex, column = 0)
        colorText = tk.Text(self, height = heightText, width = widthText)
        colorText.config(bg = self.valid)
        colorText.grid(row = rowIndex, column = 1)
        colorConfig = '^[a-zA-Z]{1,10}$'
        
        rowIndex += 1
        colorLabelErr = tk.Label(self, text = 'Invalid Color Input')
        colorLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        colorLabelErr.grid_remove()  
          
         
        rowIndex += 1  
        typeLabel = tk.Label(self, text = 'Type_id: ')
        typeLabel.grid(row = rowIndex, column = 0)
        typeText = tk.Text(self, height = heightText, width = widthText)
        typeText.config(bg = self.valid)
        typeText.grid(row = rowIndex, column = 1)
        typeConfig = '^[1-9]\d*$'      
        
        rowIndex += 1
        typeLabelErr = tk.Label(self, text = 'Invalid Type Input')
        typeLabelErr.grid(row = rowIndex, column = 0, columnspan = 2)
        typeLabelErr.grid_remove()  
        
        rowIndex += 1
        submitBtn = tk.Button(self, text = 'Submit',
                            command = lambda: combineFuncs(submit(),
                                                           validate(ownerText, ownerConfig, ownerLabelErr),
                                                           validate(secondaryText, secondaryConfig, secondaryLabelErr),
                                                           validate(serialText, serialConfig, serialLabelErr),
                                                           validate(makerText, makerConfig, makerLabelErr),
                                                           validate(modelText, modelConfig, modelLabelErr),
                                                           validate(yearText, yearConfig, yearLabelErr),
                                                           validate(colorText, colorConfig, colorLabelErr),
                                                           validate(typeText, typeConfig, typeLabelErr),
                                                           validateDBserial(serialText),
                                                           validateDBtype(typeText),
                                                           validateDBowner(ownerText),
                                                           validateDBowner(secondaryText),
                                                           pushDataToDB()))
                                                                        
        submitBtn.grid(row = rowIndex, column = 1)
        
        addOwnerBtn = tk.Button(self, text = 'Add Person',
                                command = lambda: controller.show_frame("NewPerson"))
        addOwnerBtn.grid(row = rowIndex, column = 0)
          
        rowIndex += 1    
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.grid(row = rowIndex, column = 0, columnspan = 2)
        
        def submit():
            self.isValid = True
            self.isDBValid = True
            self.vehicleData = [serialText.get('1.0','end').rstrip(),
                                '\'' + makerText.get('1.0','end').rstrip()+'\'',
                                '\'' + modelText.get('1.0','end').rstrip() +'\'',
                                yearText.get('1.0','end').rstrip(),
                                '\'' + colorText.get('1.0','end').rstrip() +'\'',
                                typeText.get('1.0','end').rstrip()]
        
        def validate(textField, regConfig, textFieldErr):
            print(textField.get('1.0','end'))
            if regex.match(regConfig,textField.get('1.0','end')):
                textField.config(bg = self.valid)
                textFieldErr.grid_remove()
            else:
                textField.config(bg = self.invalid)
                self.isValid = False
                textFieldErr.grid()
                
        def validateDBowner(textField):
            if self.isValid:
                getOwner = 'SELECT sin FROM people'
                ownerData = DBTables.getData(self, self.connectionStr, getOwner)
                compStr = str(textField.get('1.0','end'))
                for each in ownerData:
                    print(str(each))
                    if each.rstrip() == compStr.rstrip():
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

