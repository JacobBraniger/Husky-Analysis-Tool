from HuskEvent import HuskEvent
from MachineEvent import MachineEvent
from CycleInterruptEvent import CycleInterruptEvent
import pandas
from datetime import *
from tkinter import *
from tkinter import filedialog
from collections import Counter

def func1(df):
    #Populating eventList with HuskEvent objects
    eventList = [] #A list of all events
    for i in range(len(df)):
        #making temporary list to hold and manipulate each row of data
        attributes = [df.at[i, 'Date/Time'], df.at[i, 'Type'], df.at[i, 'Source'], df.at[i, 'Description']]
        for i in range(1, len(attributes)):
            if (attributes[i][0] == ' '):
                attributes[i] = attributes[i].replace(' ', '', 1)

        #Adding Machine Events
        if (attributes[1] == 'Machine'):
            eventList.append(MachineEvent(attributes[0], attributes[1], attributes[2], attributes[3]))

        #Adding Cycle Interruptions
        elif (attributes[1] == 'Cycle Interruption'):
            eventList.append(CycleInterruptEvent(attributes[0], attributes[1], attributes[2], attributes[3]))
            #
            if(type(eventList[i-1]) == MachineEvent):
                if(eventList[i-1].getType == "Cycle Interruption"):
                    eventList[i-1].setReason(eventList[i].getReason)

        #If none of the above types, makes a generic event
        else:
            eventList.append(HuskEvent(attributes[0], attributes[1], attributes[2], attributes[3]))
    #end loop
    return eventList

def func2(df):
    #Populating eventList with HuskEvent objects
    eventList = [] #A list of all events
    for i in range(len(df)):
        #making temporary list to hold and manipulate each row of data
        attributes = [df.at[i, 'Date'], df.at[i, 'Time'], df.at[i, 'Type'], df.at[i, 'Source'], df.at[i, 'Description']]

        if (" - " in attributes[2]):
            attributes[2] = attributes[2].split(' - ')[0]

        #Adding Machine Events
        if (attributes[2] == 'Machine'):
            eventList.append(MachineEvent.fiveLines(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4]))

        #Adding Cycle Interruptions
        elif (attributes[2] == 'Cycle Interruption'):
            eventList.append(CycleInterruptEvent.fiveLines(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4]))
            #
            if(type(eventList[i-1]) == MachineEvent):
                if(eventList[i-1].getType == "Cycle Interruption"):
                    eventList[i-1].setReason(eventList[i].getReason)

        #If none of the above types, makes a generic event
        else:
            eventList.append(HuskEvent.fiveLines(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4]))
    #end loop
    return eventList

def analyze():
    #Making new text file to write to
    f = open(e.get() + ".txt", "w")
    
    #Creating data frame from selected file
    workbook = filedialog.askopenfilename(parent=mainWin, initialdir= "/", title='Please select a directory')
    df = pandas.read_excel(workbook)

    if (len(df.columns) == 4):
        eventList = func1(df)
    elif (len(df.columns) == 5):
        eventList = func2(df)

    runTime = timedelta(0) #the total time that the machine has been running on auto cycle over the data period. Only counts if it was running for more than a minute
    problemList = [] #Counts up all reasons of Cycle Interruptions

    #Collecting various data from the eventList
    for i in range(len(eventList)-1):

        #Add runtime. this is based on every cycle interruption machine event having a note of what mode it came out of and when that mode was strated. 
        #counts up both cycle interruptions and when the machine is put into idle, both only if it was previously in auto mode for more than a minute.
        if (type(eventList[i]) == MachineEvent and eventList[i].getPrevState() == "Auto Cycling" and eventList[i].getLastDuration() >= minCycle):
            runTime += eventList[i].getLastDuration()
        
        #Counting up problems
        elif (type(eventList[i]) == CycleInterruptEvent and (not cycleBlackList.__contains__(eventList[i].getReason())) and (countActiveInterrupts or eventList[i].getDscrp().__contains__("Inactive"))):
            problemList.append(eventList[i].getReason())
    
    #Writing analytic data:
    #Writing total runtime
    f.write("The total runtime over the period from " + eventList[-1].getTime().strftime("%m/%d/%Y %I:%M:%S %p") + " to " + eventList[0].getTime().strftime("%m/%d/%Y %I:%M:%S %p") + " was " + str(round(runTime.total_seconds()/60/60, 3)) + " hours.\n")
    #Writing availibility
    f.write("Availibility: " + str(round(runTime / (eventList[0].getTime() - eventList[-1].getTime())*100, 2)) + "%.\n")
    #Writing total Cycle Interruptions
    f.write("Total Cycle Interruptions: " + str(len(problemList)) + ".\n")
    #Writing Cycle Interruption breakdown
    new_vals = Counter(problemList).most_common() #Makes new counter and counts up the Cycle Interruption reasons
    new_vals = new_vals[::1] #this sorts the list in descending order
    for a, b in new_vals:
        f.write(str(a) + ": " + str(b) + ", " + str(round(b/len(problemList)*100, 2)) + "%\n")
        #end
    
    # f.write("\n")
    # #Writing log to file
    # for i in range(len(eventList)-1):

    #     #Writing Machine Events to f
    #     if (type(eventList[i]) == MachineEvent):
    #         f.write(str(eventList[i]) + "\n")
        
    #     #Writing Cycle Interruptions
    #     elif (type(eventList[i]) == CycleInterruptEvent):
    #         f.write(str(eventList[i]) + "\n")

    f.close #close file
    #Generate message that writing is done
    myLabel = Label(mainWin, text = "Generated " + e.get() + " from " + workbook)
    myLabel.pack()
    #end analyze()

#Read config
conf = open("config.txt", "r")
lines = conf.readlines()
minCycle = datetime.strptime("01-01-0001 " + lines[0].split(" = ")[1].replace("\n", ""), "%d-%m-%Y %H:%M:%S") - datetime.strptime("01-01-0001 00:00:00", "%d-%m-%Y %H:%M:%S")
countActiveInterrupts = (lines[1].split(" = ")[1] == "True")
cycleBlackList = []
if (len(lines) > 3):
    for i in range(3, len(lines)):
        cycleBlackList.append(lines[i])

#Constructing the control window
mainWin = Tk()
mainWin.title("Greencastle Machine Data Analysis Tool")
mainWin.geometry("500x200")
mainWin.sourceFile = ''

#Constructing the file name entry box
e = Entry(mainWin, width=50)
e.pack()
e.insert(0, "Name Your Output File")

#analyze button
def myClick():
    analyze()
myButton1 = Button(mainWin, text = "Choose Workbook to Analyze", command = myClick)
myButton1.pack()

#quit button
def closeClick():
    mainWin.destroy()
myButton2 = Button(mainWin, text = "Quit", command = closeClick)
myButton2.pack()

mainWin.mainloop()