'''
Created on Mar 15, 2016

@author: drei
'''

import tkinter as tk
import re as regex
from DBConnect import DBTables

class NewPerson(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    isValid = False
    isDBValid = False
    connectionStr = ''
        
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
        ownerLabel = tk.Label(self, text = 'Owner SIN: ')
        ownerLabel.grid(row = rowIndex, column = 0)
        ownerText = tk.Text(self, height = heightText, width = widthText)
        ownerText.config(bg = self.valid)
        ownerText.grid(row = rowIndex, column = 1)
        ownerConfig = '^[a-zA-Z0-9]{1,15}$'
        rowIndex += 1    
        
        
        
        submitBtn = tk.Button(self, text = 'Submit')                                                          
        submitBtn.grid(row = rowIndex, column = 1)
        
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("NewVehReg"))
        backBtn.grid(row = rowIndex, column = 0)
        
#         def submit():
#             self.isValid = True
#             self.isDBValid = True
#             self.vehicleData = [serialText.get('1.0','end').rstrip(),
#                                 '\'' + makerText.get('1.0','end').rstrip()+'\'',
#                                 '\'' + modelText.get('1.0','end').rstrip() +'\'',
#                                 yearText.get('1.0','end').rstrip(),
#                                 '\'' + colorText.get('1.0','end').rstrip() +'\'',
#                                 typeText.get('1.0','end').rstrip()]
#         
#         def validate(textField, regConfig):
#             print(textField.get('1.0','end'))
#             if regex.match(regConfig,textField.get('1.0','end')):
#                 textField.config(bg = self.valid)
#             else:
#                 textField.config(bg = self.invalid)
#                 self.isValid = False
#                 
#         def validateDBowner(textField):
#             if self.isValid:
#                 getOwner = 'SELECT sin FROM people'
#                 ownerData = DBTables.getData(self, self.connectionStr, getOwner)
#                 compStr = str(textField.get('1.0','end'))
#                 for each in ownerData:
#                     print(str(each))
#                     if each.rstrip() == compStr.rstrip():
#                         self.isDBValid = False
#                         textField.config(bg = self.invalid)
#                         print('owner in DB')
#                         
#         def validateDBserial(textField):
#             if self.isValid:
#                 getSerial = 'SELECT serial_no FROM vehicle'
#                 serialData = DBTables.getData(self, self.connectionStr, getSerial)
#                 compStr = textField.get('1.0','end')
#                 for each in serialData:
#                     if int(each) == int(compStr):
#                         self.isDBValid = False
#                         textField.config(bg = self.invalid)
#                         print('serial in DB')
#         
#         def validateDBtype(textField):
#             if self.isValid:
#                 getType = 'SELECT type_id FROM vehicle_type'
#                 typeData = DBTables.getData(self, self.connectionStr, getType)
#                 intData = []
#                 for each in typeData:
#                     intData.append(int(each))
#                 compStr = int(textField.get('1.0','end'))
#                 if compStr not in intData:
#                     self.isDBValid = False
#                     textField.config(bg = self.invalid)
#                     print('type not in DB')
#                     
#                     
#         def pushDataToDB():
#             if self.isDBValid and self.isValid:
#                 insertStatement = 'INSERT INTO vehicle VALUES('
#                 for each in self.vehicleData:
#                     insertStatement += each.rstrip() + ','
#                 insertStatement = insertStatement[:-1]
#                 insertStatement += ')'
#                 print(insertStatement)
#                 DBTables.pushData(self, self.connectionStr, insertStatement)
#                 
#         def combineFuncs(*funcs):
#             def combinedFunc(*args, **kwargs):
#                 for f in funcs:
#                     f(*args, **kwargs)
#             return combinedFunc