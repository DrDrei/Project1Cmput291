import tkinter as tk
import re as regex
from DBConnect import DBTables

class DLReg(tk.Frame):
    
    valid = 'light grey'
    connectionStr = ''
    isValid = False
    DLData = []
    def __init__(self, connectionStr, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.connectionStr = connectionStr
        
        textWidth = 20
        textHeight = 1
        rowIndex = 0        

        label = tk.Label(self, text = 'Driver License Registration:')
        label.grid(row = rowIndex, column = 0, columnspan = 2)
        
        rowIndex += 1
        licenseLabel = tk.Label(self, text = 'License Number: ')
        licenseLabel.grid(row = rowIndex, column = 0)
        licenseText = tk.Text(self, height = textHeight, width = textWidth)
        licenseText.config(bg = self.valid)
        licenseText.grid(row = rowIndex, column = 1)
        licenseConfig = '^[0-9]{1,15}$'  
        
        rowIndex += 1
        sinLabel = tk.Label(self, text = 'SIN number: ')
        sinLabel.grid(row = rowIndex, column = 0)
        sinText = tk.Text(self, height = textHeight, width = textWidth)
        sinText.config(bg = self.valid)
        sinText.grid(row = rowIndex, column = 1)
        sinConfig = '^[0-9]{1,15}$'  
        
        rowIndex += 1
        classLabel = tk.Label(self, text = 'Class: ')
        classLabel.grid(row = rowIndex, column = 0)
        classText = tk.Text(self, height = textHeight, width = textWidth)
        classText.config(bg = self.valid)
        classText.grid(row = rowIndex, column = 1)
        classConfig = '^[a-zA-Z0-9]{1,10}$' 
        
        rowIndex += 1
        photoLabel = tk.Label(self, text = 'Photo: ')
        photoLabel.grid(row = rowIndex, column = 0)
        photoText = tk.Text(self, height = textHeight, width = textWidth)
        photoText.config(bg = self.valid)
        photoText.grid(row = rowIndex, column = 1)
        photoConfig = '^[a-zA-Z]{1,15}$' 
                
        rowIndex += 1
        issueLabel = tk.Label(self, text = 'Issue date: ')
        issueLabel.grid(row = rowIndex, column = 0)
        issueText = tk.Text(self, height = textHeight, width = textWidth)
        issueText.config(bg = self.valid)
        issueText.grid(row = rowIndex, column = 1)
        issueConfig = '^(19|20)\d\d(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$' 
                
        rowIndex += 1
        expireLabel = tk.Label(self, text = 'Expiry date: ')
        expireLabel.grid(row = rowIndex, column = 0)
        expireText = tk.Text(self, height = textHeight, width = textWidth)
        expireText.config(bg = self.valid)
        expireText.grid(row = rowIndex, column = 1)
        expireConfig = '^(19|20)\d\d(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$' 
                        
        rowIndex += 1
        submitBtn = tk.Button(self, text = 'Submit',
                              command = lambda: combineFuncs(submit(),
                                                            validate(licenseText, licenseConfig),
                                                            validate(sinText, sinConfig),
                                                            validate(classText, classConfig),
                                                            validate(photoText, photoConfig),
                                                            validate(issueText, issueConfig),
                                                            validate(expireText, expireConfig),
                                                            validateDBlicense(licenseText),
                                                            validateDBsin(sinText),
                                                            pushToDB()))
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
            self.DLData = [licenseText.get('1.0','end').rstrip(),
                            sinText.get('1.0','end').rstrip(),
                            '\'' + classText.get('1.0','end').rstrip() +'\'',
                            '\'' + photoText.get('1.0','end').rstrip() +'\'',
                            'TO_DATE(\'' + issueText.get('1.0','end').rstrip() +'\', \'YYYYMMDD\')',
                            'TO_DATE(\'' + expireText.get('1.0','end').rstrip() +'\', \'YYYYMMDD\')']   
            
        def validate(textField, regConfig):
            print('user input', textField.get('1.0','end'))
            if not regex.match(regConfig, textField.get('1.0','end')):
                print(textField,"Field not valid")     
                self.isValid = False     
                    
        def validateDBlicense(textField):
            getLicense = 'SELECT licence_no FROM drive_licence'
            licenseData = DBTables.getData(self, self.connectionStr, getLicense)
            license = textField.get('1.0', 'end').rstrip()
            for i in range(len(licenseData)):
                index = licenseData[i].index(" ")
                licenseData[i] = licenseData[i][:index]
            if str(license) in licenseData:
                print("Invalid: License number already exists for this person!")
                self.isValid = False
            else:
                print("Adding new license... ")
                
        def validateDBsin(textField):
            getSin = 'SELECT sin FROM people'
            sinData = DBTables.getData(self, self.connectionStr, getSin)
            sin = textField.get('1.0', 'end').rstrip()
            for i in range(len(sinData)):
                index = sinData[i].index(" ")
                sinData[i] = sinData[i][:index]
            if str(sin) in sinData:
                print("sin # exists")
            else:
                print("Invalid: SIN Number does not exist, try adding a new person")
                self.isValid = False 
                
        def pushToDB():
            if self.isValid:
                insertStatement = 'insert into drive_licence values('
                for each in self.DLData:
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