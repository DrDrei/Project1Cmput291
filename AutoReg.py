import tkinter as tk
import re as regex
from DBConnect import DBTables
import time
        
class AutoReg(tk.Frame):
    valid = 'light grey'
    invalid = 'red'
    isValid = False
    autoData = ['','','','']
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
        primaryLabel = tk.Label(self, text = 'Owner SIN: ')
        primaryLabel.grid(row = rowIndex, column = 0)
        primaryText = tk.Text(self, height = heightText, width = widthText)
        primaryText.config(bg = self.valid)
        primaryText.grid(row = rowIndex, column = 1)
        primaryConfig = '^[0-9A-Za-z]{1,15}$'
        
        rowIndex += 1
        buyerLabel = tk.Label(self, text = 'Buyer SIN: ')
        buyerLabel.grid(row = rowIndex, column = 0)
        buyerText = tk.Text(self, height = heightText, width = widthText)
        buyerText.config(bg = self.valid)
        buyerText.grid(row = rowIndex, column = 1)
        buyerConfig = '^[0-9A-Za-z]{1,15}$'
        
        rowIndex += 1
        vehicleLabel = tk.Label(self, text = 'Vehicle ID: ')
        vehicleLabel.grid(row = rowIndex, column = 0)
        vehicleText = tk.Text(self, height = heightText, width = widthText)
        vehicleText.config(bg = self.valid)
        vehicleText.grid(row = rowIndex, column = 1)
        vehicleConfig = '^[0-9A-Za-z]{1,15}$'
        
        rowIndex += 1
        priceLabel = tk.Label(self, text = 'Price: ')
        priceLabel.grid(row = rowIndex, column = 0)
        priceText = tk.Text(self, height = heightText, width = widthText)
        priceText.config(bg = self.valid)
        priceText.grid(row = rowIndex, column = 1)
        priceConfig = '^\d{1,9}(\.\d{1,2})?$'
        
        rowIndex += 1
        submitBtn = tk.Button(self, text = 'Submit',
                            command = lambda: combineFuncs(submit(),
                                                           validate(primaryText, primaryConfig),
                                                           validate(buyerText, buyerConfig),
                                                           validate(vehicleText, vehicleConfig),
                                                           validate(priceText, priceConfig),
                                                           validateBuyer(buyerText),
                                                           validatePrice(priceText),
                                                           validateOwner(primaryText, vehicleText),
                                                           deleteFromDB(),
                                                           pushToDB()
                                                           ))                                                                
        submitBtn.grid(row = rowIndex, column = 1)
        
        addOwnerBtn = tk.Button(self, text = 'Add Person',
                                command = lambda: controller.show_frame("NewPerson2"))
        addOwnerBtn.grid(row = rowIndex, column = 0)
          
        rowIndex += 1    
        backBtn = tk.Button(self, text = 'Back',
                            command = lambda: controller.show_frame("MainMenu"))
        backBtn.grid(row = rowIndex, column = 0, columnspan = 2)
        
        def submit():
            self.isValid = True
            
        def validateOwner(ownerField, vehicleField):
            if ownerField.get('1.0','end').rstrip() != '\n' and vehicleField.get('1.0','end').rstrip() != '/n':
                owner = ownerField.get('1.0','end').rstrip()
                vehicle = vehicleField.get('1.0','end').rstrip()
                getStmt = 'select * from owner where vehicle_id=' + vehicle +' and owner_id=' + owner + ' and is_primary_owner=\'y\''
                stmtData = DBTables.getRawData(self, self.connectionStr, getStmt)
                if len(stmtData) > 0:
                    self.autoData[0] = owner
                    self.autoData[2] = vehicle
                else:
                    print('owner does not own this vehicle')
                    self.isValid = False
                print(self.autoData)

        def validateBuyer(textField):
            if textField.get('1.0', 'end').rstrip() != '\n':
                buyer = textField.get('1.0', 'end').rstrip()
                getStmt = 'select sin from people'
                stmtData = DBTables.getData(self, self.connectionStr, getStmt)
                for i, item in enumerate(stmtData):
                    stmtData[i] = item.rstrip()
                if buyer in stmtData:
                    self.autoData[1] = buyer
                else:
                    self.isValid = False
                    print('buyer is not in the database')
        
        def validatePrice(textField):
            if textField.get('1.0', 'end').rstrip() != '\n':
                price = textField.get('1.0', 'end').rstrip()
                self.autoData[3] = price
                                
                
        def validate(textField, regConfig):
            print(textField.get('1.0','end'))
            if regex.match(regConfig,textField.get('1.0','end')):
                textField.config(bg = self.valid)
            else:
                textField.config(bg = self.invalid)
                self.isValid = False
                                
        def deleteFromDB():
            if self.isValid:
                getStmt = 'delete from owner where owner_id=' + self.autoData[0] + ' and vehicle_id=' + self.autoData[2]
                stmtData = DBTables.pushData(self, self.connectionStr, getStmt)
            
        def pushToDB():
            if self.isValid:
                print('insert')
                getStmt = 'insert into owner values(' + self.autoData[1] + ',' +self.autoData[2] + ',\'y\')'
                DBTables.pushData(self, self.connectionStr, getStmt)
                
                getStmt = 'select max(transaction_id) from auto_sale'
                getIndex = DBTables.getData(self, self.connectionStr, getStmt)
                
                nowTime = time.strftime('%Y%m%d')
                print(nowTime)
                newStmt = 'insert into auto_sale values('   + str(getIndex[0]+1) + ',' + self.autoData[0] + ',' + self.autoData[1] + ','+ self.autoData[2]+ ',' + 'TO_DATE(\'' + nowTime + '\', \'YYYYMMDD\')' + ','+ self.autoData[3] + ')'
                print(newStmt)
                DBTables.pushData(self, self.connectionStr, newStmt)
                
        def combineFuncs(*funcs):
            def combinedFunc(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combinedFunc

