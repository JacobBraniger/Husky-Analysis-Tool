from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from Analyzer import *

#Some presets, usually handled via the config. This file is made to be turned into a standalone exe, so does not get a config.
config = []
config.append(timedelta(minutes=1))
config.append(False)
config.append(["Auto Purge completed"])

#Constructing the control window
mainWin = Tk()
mainWin.title("Greencastle Machine Data Analysis Tool")
mainWin.geometry("550x300")
mainWin.sourceFile = ''
mainWin.iconbitmap("DogFace.ico")
#This is a buffer that starts the pack command below the following dialog boxes. 
#This is needed for the error and confirmation messages to not cover the rest of the UI.
myLabel = Label(mainWin, text = '', fg='red', pady =  55, justify='left')
myLabel.pack()

#Constructing the file name entry box
inputBox = Entry(mainWin, width=67)
inputBox.insert(0, "File To Analyze")
inputBox.place(x = 10, y = 12.5)

def chooseInput(Box = inputBox):
    #Choose input file. Chosen file must be an excel workbook.
    global inputFile1 #String
    inputFile1 = filedialog.askopenfilename(parent=mainWin, initialdir= "/", title='Please select a directory', filetypes=(("excel workbooks","*.xlsx"), ("all files","*.*")))
    #clear and replace the box
    inputBox.delete(0, 'end')
    Box.insert(0, inputFile1)
#Choose File Button
myButton1 = Button(mainWin, text = "Choose File", command = chooseInput)
myButton1.place(x = 430, y = 10)

#Constructing the output location entry box
outputBox = Entry(mainWin, width=67)
outputBox.insert(0, "Output Folder")
outputBox.place(x = 10, y = 52.5)

def chooseFolder(Box = outputBox):
    global outputLoc1
    outputLoc1 = askdirectory(title='Select Folder')
    Box.delete(0, 'end')
    Box.insert(0, outputLoc1)
myButton2 = Button(mainWin, text = "Choose Folder", command = chooseFolder)
myButton2.place(x = 430, y = 50)

nameBox = Entry(mainWin, width=67)
nameBox.insert(0, "Name Your Output File")
nameBox.place(x = 10, y = 92.5)
#analyze button
def analyButton():
    try:
        analyze(mainWin, nameBox, inputFile1, outputLoc1, config)
    except NameError:
        myLabel = Label(mainWin, text = 'Some files were not chosen. Please choose an input file and output location.', fg='red', justify='left')
        myLabel.pack()
        return
myButton3 = Button(mainWin, text = "Analyze!", command = analyButton)
myButton3.place(x = 430, y = 90)

mainWin.mainloop()