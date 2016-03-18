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
        sinLabel = tk.Label(self, text = 'SIN Number: ')
        sinLabel.grid(row = rowIndex, column = 0)
        sinText = tk.Text(self, height = heightText, width = widthText)
        sinText.config(bg = self.valid)
        sinText.grid(row = rowIndex, column = 1)
        sinConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1       
        serialLabel = tk.Label(self, text = 'Serial Number: ')
        serialLabel.grid(row = rowIndex, column = 0)
        serialText = tk.Text(self, height = heightText, width = widthText)
        serialText.config(bg = self.valid)
        serialText.grid(row = rowIndex, column = 1)
        serialConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        submitBtn = tk.Button(self, text = 'Search',
                            command = lambda: combineFuncs(searchName(nameText),
                                                           searchLicence(licenseText),
                                                           searchSin(sinText),
                                                           searchSerial(serialText)))                                                                
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
            if nameField.get('1.0') != '\n':
                getStatement = 'select name, licence_no, addr, birthday, class, expiring_date from people p, drive_licence dl where p.sin=dl.sin and name=\''
                compStr = nameField.get('1.0','end').rstrip() + '\''
                getStatement += compStr
                serialData = DBTables.getRawData(self, self.connectionStr, getStatement)
                if len(serialData) > 0:
                    for each in serialData:
                        printFound(each)
                else:
                    print('No such names in Database')
            
        def searchLicence(licenceField):    
            if licenceField.get('1.0') != '\n':    
                getStatement = 'select name, licence_no, addr, birthday, class, expiring_date from people p, drive_licence dl where p.sin=dl.sin and licence_no='
                compStr = licenceField.get('1.0','end').rstrip()
                getStatement += compStr
                serialData = DBTables.getRawData(self, self.connectionStr, getStatement)
                if len(serialData) > 0:
                    for each in serialData:
                        printFound(each)
                else:
                    print('No such license in Database')
                
                getStatement = 'select ticket_no from ticket t, drive_licence dl where dl.sin=t.violator_no and dl.licence_no='
                getStatement += compStr
                serialData = DBTables.getData(self, self.connectionStr, getStatement)
                if len(serialData) > 0:
                    print('Violations IDs received by ' + compStr + ': ')
                    for each in serialData:
                        print(each)
                else:
                    print('No tickets received by this sin')
                    
        def searchSin(sinField):
            if sinField.get('1.0') != '\n':
                getStatement = 'select ticket_no from ticket t where t.violator_no='
                compStr = sinField.get('1.0','end').rstrip()
                getStatement += compStr
                serialData = DBTables.getData(self, self.connectionStr, getStatement)
                if len(serialData) > 0:
                    print('Violations IDs received by ' + compStr)
                    for each in serialData:
                        print(each)
                else:
                    print('No tickets received by this sin')
                    
        def searchSerial(serialField):
            if serialText.get('1.0') != '\n':
                getStatement = 'select price from auto_sale where vehicle_id='
                compStr = serialField.get('1.0','end').rstrip()
                getStatement += compStr
                Data = DBTables.getData(self, self.connectionStr, getStatement)
                getStatement = 'select vehicle_id from ticket where vehicle_id='
                getStatement += compStr
                numViolations = DBTables.getData(self, self.connectionStr, getStatement)
                if len(Data) > 0:
                    print('Sold ' + str(len(Data)) + ' times. Average selling price is ' + str(sum(Data) / float(len(Data))) + '. Number of violations ' + str(len(numViolations)))
                else:
                    print('No such license number exists.')
#                     print('Sold 0 times. Average selling price is unknown. Number of violations ' + str(len(numViolations)))
                
        def printFound(each):
            name, licence, addr, bday, klass, expiry = each
            licStr = str(licence).rstrip()
            conditions = checkCondition(licStr)
            print('Name: '+name+' License: '+str(licence).rstrip()+' Address: '+addr+' Birthday: '+str(bday)+' Class: '+klass+' Conditions: '+conditions+' Expiry: '+str(expiry))
                 
        def checkCondition(licence): 
            condStatement = 'select description from driving_condition dc, restriction r where dc.c_id=r.r_id and licence_no=\''
            licStr = licence + '\''
            condStatement += licStr
            condData = DBTables.getData(self, self.connectionStr, condStatement)
            conditions = '('
            if len(condData) > 0:
                for each in condData:
                    conditions += each
                    conditions += ','
                conditions = conditions[:-1]
                conditions += ')'
                return conditions
            else:
                return '(no conditions)' 
                    
        def combineFuncs(*funcs):
            def combinedFunc(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combinedFunc
