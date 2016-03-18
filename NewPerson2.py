'''
Created on Mar 15, 2016

@author: drei
'''

import tkinter as tk
import datetime
import re as regex
from DBConnect import DBTables
from cgi import valid_boundary


class NewPerson2(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    isInputValid = False
    isDBValid = False
    personData =[]
    connectionStr = ''
        
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.connectionStr = connectionStr
        
        textWidth = 20
        textHeight = 1
        rowIndex = 0
        
        label = tk.Label(self, text = 'Register a new Person:')
        label.grid(row = rowIndex, column = 0, columnspan = 2)
        
        rowIndex += 1
        sinLabel = tk.Label(self, text = 'Person SIN: ')
        sinLabel.grid(row = rowIndex, column = 0)
        sinText = tk.Text(self, height = textHeight, width = textWidth)
        sinText.config(bg = self.valid)
        sinText.grid(row = rowIndex, column = 1)
        sinConfig = '^[0-9]{1,15}$'
        
        rowIndex += 1
        nameLabel = tk.Label(self, text = 'Name: ')
        nameLabel.grid(row = rowIndex, column = 0)
        nameText = tk.Text(self, height = textHeight, width = textWidth)
        nameText.config(bg = self.valid)
        nameText.grid(row = rowIndex, column = 1)
        nameConfig = '^[a-zA-Z]{1,40}$'
        
        rowIndex += 1    
        heightLabel = tk.Label(self, text = 'Height: ')
        heightLabel.grid(row = rowIndex, column = 0)
        heightText = tk.Text(self, height = textHeight, width = textWidth)
        heightText.config(bg = self.valid)
        heightText.grid(row = rowIndex, column = 1)
        heightConfig = '^\d{1,5}(\.\d{1,2})?$'
        
        rowIndex += 1    
        weightLabel = tk.Label(self, text = 'Weight: ')
        weightLabel.grid(row = rowIndex, column = 0)
        weightText = tk.Text(self, height = textHeight, width = textWidth)
        weightText.config(bg = self.valid)
        weightText.grid(row = rowIndex, column = 1)
        weightConfig = '^\d{1,5}(\.\d{1,2})?$'
        
        rowIndex += 1    
        eyeLabel = tk.Label(self, text = 'Eye Color: ')
        eyeLabel.grid(row = rowIndex, column = 0)
        eyeText = tk.Text(self, height = textHeight, width = textWidth)
        eyeText.config(bg = self.valid)
        eyeText.grid(row = rowIndex, column = 1)
        eyeConfig = '^[a-zA-Z]{3,10}$'
        
        rowIndex += 1    
        hairLabel = tk.Label(self, text = 'Hair Color: ')
        hairLabel.grid(row = rowIndex, column = 0)
        hairText = tk.Text(self, height = textHeight, width = textWidth)
        hairText.config(bg = self.valid)
        hairText.grid(row = rowIndex, column = 1)
        hairConfig = '^[a-zA-Z]{3,10}$'
        
        rowIndex += 1    
        addrLabel = tk.Label(self, text = 'Address: ')
        addrLabel.grid(row = rowIndex, column = 0)
        addrText = tk.Text(self, height = textHeight, width = textWidth)
        addrText.config(bg = self.valid)
        addrText.grid(row = rowIndex, column = 1)
        addrConfig = '^.{1,20}$'
        
        rowIndex += 1    
        genderLabel = tk.Label(self, text = 'Gender [m/f]: ')
        genderLabel.grid(row = rowIndex, column = 0)
        genderText = tk.Text(self, height = textHeight, width = textWidth)
        genderText.config(bg = self.valid)
        genderText.grid(row = rowIndex, column = 1)
        genderConfig = '^([m]|[f]){1,1}$'
        
        rowIndex += 1    
        bdayLabel = tk.Label(self, text = 'Birthday [yyyymmdd]: ')
        bdayLabel.grid(row = rowIndex, column = 0)
        bdayText = tk.Text(self, height = textHeight, width = textWidth)
        bdayText.config(bg = self.valid)
        bdayText.grid(row = rowIndex, column = 1)
        bdayConfig = '^(19|20)\d\d(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$'
        
        rowIndex += 1    
        submitBtn = tk.Button(self, text = 'Submit', command = lambda: combineFuncs(submit(),
                                                                                    validate(sinText, sinConfig),
                                                                                    validate(nameText, nameConfig),
                                                                                    validate(heightText, heightConfig),
                                                                                    validate(weightText, weightConfig),
                                                                                    validate(eyeText, eyeConfig),
                                                                                    validate(hairText, hairConfig),
                                                                                    validate(addrText, addrConfig),
                                                                                    validate(genderText, genderConfig),
                                                                                    validate(bdayText, bdayConfig),
                                                                                    validateDBsin(sinText),
                                                                                    pushDataToDB()))                                                          
        submitBtn.grid(row = rowIndex, column = 1)
        
        backBtn = tk.Button(self, text = 'Back', command = lambda: controller.show_frame('AutoReg'))
        backBtn.grid(row = rowIndex, column = 0)
        
        def submit():
            self.isInputValid = True
            self.isDBValid = True
            self.personData = [sinText.get('1.0','end').rstrip(),
                               '\'' + nameText.get('1.0', 'end').rstrip() + '\'',
                                heightText.get('1.0','end').rstrip(),
                                weightText.get('1.0','end').rstrip(),
                                '\'' + eyeText.get('1.0','end').rstrip() +'\'',
                                '\'' + hairText.get('1.0','end').rstrip() +'\'',
                                '\'' + addrText.get('1.0','end').rstrip() +'\'',
                                '\'' + genderText.get('1.0','end').rstrip() +'\'',
                                'TO_DATE(\'' + bdayText.get('1.0','end').rstrip() +'\', \'YYYYMMDD\')']
         
        def validate(textField, regConfig):
            print(textField.get('1.0','end'))
            if regex.match(regConfig,textField.get('1.0','end')):
                textField.config(bg = self.valid)
            else:
                textField.config(bg = self.invalid)
                self.isInputValid = False
                          
        def validateDBsin(textField):
            if self.isInputValid:
                getSerial = 'SELECT sin FROM people'
                serialData = DBTables.getData(self, self.connectionStr, getSerial)
                compStr = textField.get('1.0','end')
                for each in serialData:
                    print(each)
                    if each.rstrip() == compStr.rstrip():
                        self.isDBValid = False
                        textField.config(bg = self.invalid)
                        print('sin in DB')
                         
        def pushDataToDB():
            if self.isDBValid and self.isInputValid:
                insertStatement = 'INSERT INTO people VALUES('
                for each in self.personData:
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