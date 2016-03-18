'''
Created on Mar 10, 2016

@author: drei
'''
import tkinter as tk
import re as regex
from DBConnect import DBTables

class VioReg(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    isValid = False
    pushData = []
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.connectionStr = connectionStr
        widthText = 20
        heightText = 1
        rowIndex = 0
        
        label = tk.Label(self, text = 'Violation Record registration: ')
        label.grid(row = rowIndex, column = 0, columnspan = 2)
        
        rowIndex += 1
        driverLabel = tk.Label(self, text = 'Driver License (empty if none): ')
        driverLabel.grid(row = rowIndex, column = 0)
        driverText = tk.Text(self, height = heightText, width = widthText)
        driverText.config(bg = self.valid)
        driverText.grid(row = rowIndex, column = 1)
        driverConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        vehicleLabel = tk.Label(self, text = 'Vehicle Serial: ')
        vehicleLabel.grid(row = rowIndex, column = 0)
        vehicleText = tk.Text(self, height = heightText, width = widthText)
        vehicleText.config(bg = self.valid)
        vehicleText.grid(row = rowIndex, column = 1)
        vehicleConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        officerLabel = tk.Label(self, text = 'Officer SIN: ')
        officerLabel.grid(row = rowIndex, column = 0)
        officerText = tk.Text(self, height = heightText, width = widthText)
        officerText.config(bg = self.valid)
        officerText.grid(row = rowIndex, column = 1)
        officerConfig = '^[a-zA-Z0-9]{1,15}$'
        
        rowIndex += 1
        typeLabel = tk.Label(self, text = 'Violation Type (int): ')
        typeLabel.grid(row = rowIndex, column = 0)
        typeText = tk.Text(self, height = heightText, width = widthText)
        typeText.config(bg = self.valid)
        typeText.grid(row = rowIndex, column = 1)
        typeConfig = '^[0-9]{1,}$'
        
        rowIndex += 1
        dateLabel = tk.Label(self, text = 'Date: ')
        dateLabel.grid(row = rowIndex, column = 0)
        dateText = tk.Text(self, height = heightText, width = widthText)
        dateText.config(bg = self.valid)
        dateText.grid(row = rowIndex, column = 1)
        dateConfig = '^(19|20)\d\d(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$'
        
        rowIndex += 1
        placeLabel = tk.Label(self, text = 'Place of Violation: ')
        placeLabel.grid(row = rowIndex, column = 0)
        placeText = tk.Text(self, height = heightText, width = widthText)
        placeText.config(bg = self.valid)
        placeText.grid(row = rowIndex, column = 1)
        placeConfig = '^.{1,20}'
        
        rowIndex += 1
        descLabel = tk.Label(self, text = 'Notes: ')
        descLabel.grid(row = rowIndex, column = 0)
        descText = tk.Text(self, height = 5, width = widthText)
        descText.config(bg = self.valid)
        descText.grid(row = rowIndex, column = 1)
        descConfig = '^.{1,1024}$'
        
        rowIndex += 1
        submitBtn = tk.Button(self, text = 'Submit',
                            command = lambda: combineFuncs(validate(vehicleText, vehicleConfig),
                                                           validate(officerText, officerConfig),
                                                           validate(typeText, typeConfig),
                                                           validate(dateText, dateConfig),
                                                           validate(placeText, placeConfig),
                                                           validate(descText, descConfig),
                                                           submit(),
                                                           pushToDB()
                                                           ))
        submitBtn.grid(row = rowIndex, column = 1)

        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.grid(row = rowIndex, column = 0)
        
        def validate(textField, regConfig):
            if regex.match(regConfig,textField.get('1.0','end').rstrip()):
                textField.config(bg = self.valid)
            else:
                textField.config(bg = self.invalid)
                self.isValid = False
        
        def submit():
            self.isValid = True
            self.pushData = [str(checkNextTktNumber()+1),
                             validateDBdriver(driverText, vehicleText),
                             vehicleText.get('1.0','end').rstrip(),
                             officerText.get('1.0', 'end').rstrip(),
                             typeText.get('1.0', 'end').rstrip(),
                             'TO_DATE(\'' + dateText.get('1.0','end').rstrip() +'\', \'YYYYMMDD\')',
                             '\'' + placeText.get('1.0', 'end').rstrip() +'\'',
                             '\'' + descText.get('1.0', 'end').rstrip() +'\'']
            
            
        def validateDBdriver(textField, vehicleField):
            if textField.get('1.0') == '\n':
                vData = validateDBserial(vehicleField)
                if len(vData) > 0:
                    for each in vData:
                        if (each[2] == 'y'):
                            ownerID = each[0].rstrip()
                            return ownerID
                else:
                    print('no such serial number')
            else:
                getOwner = 'SELECT sin FROM people'
                ownerData = DBTables.getData(self, self.connectionStr, getOwner)
                compStr = str(textField.get('1.0','end').rstrip())
                for i, item in enumerate(ownerData):
                    ownerData[i] = item.rstrip()
                if compStr not in ownerData:
                    self.isValid = False
                    print('owner not in DB')
                else:
                    return compStr
                return('')
            
                
        def validateDBserial(textField):
            if textField.get('1.0','end') != '\n':
                getStmt = 'select * from owner where vehicle_id='
                compStr = textField.get('1.0','end').rstrip()
                getStmt += compStr
                stmtData = DBTables.getRawData(self, self.connectionStr, getStmt)
                if len(stmtData) < 1:
                    print('no such serial')
                    self.isValid = False
                return stmtData
            else:
                return []
            
                
        def validateDBofficer(textField):
            if textField.get('1.0') != '\n':
                print('validate db serial')
        
        def validateDBtype(textField):
            if textField.get('1.0') != '\n':
                print('validate db serial')
        
        def pushToDB():
            if self.isValid:
                insertStatement = 'INSERT INTO ticket VALUES('
                for each in self.pushData:
                    insertStatement += each.rstrip() + ','
                insertStatement = insertStatement[:-1]
                insertStatement += ')'
                DBTables.pushData(self, self.connectionStr, insertStatement)
                print('Ticket Added to DB')
            else:
                print('invalid input in one of the fields')
        
        
        def checkNextTktNumber():
            getStmt = 'select max(ticket_no) from ticket'
            stmtData = DBTables.getData(self, self.connectionStr, getStmt)
            return stmtData[0]
                
        def combineFuncs(*funcs):
            def combinedFunc(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combinedFunc

