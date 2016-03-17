'''
Created on Mar 10, 2016

@author: drei
'''

import tkinter as tk
import re as regex
from DBConnect import DBTables

class SearchEng(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.connectionStr = connectionStr
        widthText = 20
        heightText = 1
        rowIndex = 0
        
        label = tk.Label(self, text = 'Search Engine: Choose One.')
        label.grid(row = rowIndex, column = 0, columnspan = 2)        
        
        rowIndex += 1
        nameLabel = tk.Label(self, text = 'Name: ')
        nameLabel.grid(row = rowIndex, column = 0)
        nameText = tk.Text(self, height = heightText, width = widthText)
        nameText.config(bg = self.valid)
        nameText.grid(row = rowIndex, column = 1)
        nameConfig = '^.{1,40}$'
        
        rowIndex += 1
        licenseLabel = tk.Label(self, text = 'License Number: ')
        licenseLabel.grid(row = rowIndex, column = 0)
        licenseText = tk.Text(self, height = heightText, width = widthText)
        licenseText.config(bg = self.valid)
        licenseText.grid(row = rowIndex, column = 1)
        licenseConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        submitBtn = tk.Button(self, text = 'Search',
                            command = lambda: searchName(nameText))                                                                
        submitBtn.grid(row = rowIndex, column = 1)
        
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.grid(row = rowIndex, column = 0)
        
        def validate(textField, regConfig, textFieldErr):
            if regex.match(regConfig,textField.get('1.0','end').rstrip()):
                textField.config(bg = self.valid)
                textFieldErr.grid_remove()
            else:
                textField.config(bg = self.invalid)
                self.isValid = False
                textFieldErr.grid()
                
        def searchName(nameField):
            getStatement = 'select name, licence_no, addr, birthday, class, expiring_date from people p, drive_licence dl where p.sin=dl.sin and name=\''
            compStr = nameField.get('1.0','end').rstrip() + '\''
            getStatement += compStr
            print(getStatement)
            serialData = DBTables.getRawData(self, self.connectionStr, getStatement)
            print(serialData)
            for each in serialData:
                try:
                    print(each.rstrip())
                except:
                    print(each)
            
            
            
            
            
            
            
            
            
            
            