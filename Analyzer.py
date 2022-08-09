from HuskEvent import HuskEvent
from MachineEvent import MachineEvent
from CycleInterruptEvent import CycleInterruptEvent
import pandas as pd
from datetime import *
from tkinter import *
from collections import Counter

def read4Lines(data):
    """
    read4Lines(data)

    Takes in the type of data produced by the older types of Husky machines and converts it to a simple list made of HuskEvent objects.
    """
    #Populating eventList with HuskEvent objects
    eventList = [] #A list of all events
    for i in range(len(data)):
        #making temporary list to hold and manipulate each row of data
        attributes = [data.at[i, 'Date/Time'], data.at[i, 'Type'], data.at[i, 'Source'], data.at[i, 'Description']]
        #Removing spaces at the start of each data point. This is necessary because the titles are delineated with ",", but the data with ", "
        for j in range(1, len(attributes)):
            if (attributes[j][0] == ' '):
                attributes[j] = attributes[j].replace(' ', '', 1)

        #Adding Machine Events
        if (attributes[1] == 'Machine'):
            eventList.append(MachineEvent(attributes[0], attributes[1], attributes[2], attributes[3]))

        #Adding Cycle Interruptions
        elif (attributes[1] == 'Cycle Interruption'):
            eventList.append(CycleInterruptEvent(attributes[0], attributes[1], attributes[2], attributes[3]))
            #Adding the reason for the stoppage to the following machine event
            if(len(eventList) >= 2 and type(eventList[i-1]) == MachineEvent):
                if(eventList[i-1].getPrevState() == "Cycle Interruption"):
                    eventList[i-1].setReason(eventList[i].getReason())

        #If none of the above types, makes a generic event
        else:
            eventList.append(HuskEvent(attributes[0], attributes[1], attributes[2], attributes[3]))
    return eventList
    #end read4Lines()

def read5Lines(data):
    """
    read5Lines(data)

    Takes in the type of data produced by the newer types of Husky machines and converts it to a simple list made of HuskEvent objects. This type of output contains 5 lines of data, splitting the date and time into two columns.
    """
    #Populating eventList with HuskEvent objects
    eventList = [] #A list of all events
    for i in range(len(data)):
        #making temporary list to hold and manipulate each row of data
        attributes = [data.at[i, 'Date'], data.at[i, 'Time'], data.at[i, 'Type'], data.at[i, 'Source'], data.at[i, 'Description']]
        #Taking off the tag on some event types
        if (" - " in attributes[2]):
            attributes[2] = attributes[2].split(' - ')[0]

        #Adding Machine Events
        if (attributes[2] == 'Machine'):
            eventList.append(MachineEvent.fiveLines(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4]))

        #Adding Cycle Interruptions
        elif (attributes[2].__contains__('Cycle Interruption')):
            eventList.append(CycleInterruptEvent.fiveLines(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4]))
            if(len(eventList) >= 2 and type(eventList[i-1]) == MachineEvent):
                if(eventList[i-1].getPrevState() == "Cycle Interruption"):
                    eventList[i-1].setReason(eventList[i].getReason())

        #If none of the above types, makes a generic event
        else:
            eventList.append(HuskEvent.fiveLines(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4]))
    return eventList
    #end read5Lines()

def analyze(mainWin, nameBox, inputFile, outputLoc, config):
    """
    analyze(mainWin, nameBox, inputfile, outputLoc, config)

    Analyzes a .xlsx file, and makes a new .xlsx file with the analysis. Outputs a message when done.

    The analysis contains the following metrics:
        Start Time:
            The time of the very first event used in the analysis.
        End Time:
            The time of the very last event used in the analysis.
        Run Time:
            The total amount of time spent in the Auto Cycling state. However, an event of Auto Cycling only counts if it's longer than the minimum length defined in the config.
        Availibility:
            The percent of the time between the start and end times the was spent running.
        Total Cycle Interruptions:
            The total number of cycle interruptions in the time period. May or may not include interruptions marked as Inactive, depending on the config.
        Cycle Interruption Breakdown:
            A count of each type of cycle interruption, organized in descending order.

    Parameters:
        mainWin(Tk): the tkinter window to write the completion message on.
        nameBox(Entry): the input box to draw the output file name file from.
        inputfile(string): the file path of the file to analyze.
        outputLoc(string): the path of the folder to put the new file in.
        config(List): a list of different configuration settings.
    """
    #Turn excel file into a DataFrame
    try:
        data = pd.read_excel(inputFile)
    except FileNotFoundError:
        myLabel = Label(mainWin, text = 'File was not properly defined.', fg='red', justify='left')
        myLabel.pack()
        return
    except NameError:
        myLabel = Label(mainWin, text = 'File was not properly defined.', fg='red', justify='left')
        myLabel.pack()
        return
    except ValueError:
        myLabel = Label(mainWin, text = 'Not an excel file of the correct version. Please choose a .xlsx file.', fg='red', justify='left')
        myLabel.pack()
        return
    except Exception:
        myLabel = Label(mainWin, text = 'Something inexplicably went wrong.', fg='red', justify='left')
        myLabel.pack()
        return

    #Check if folder is blank (happens when someone closes the folder selection window without choosing)
    if (outputLoc == ''):
        myLabel = Label(mainWin, text = 'Please select an output location.', fg='red', justify='left')
        myLabel.pack()
        return

    #reading data
    if (len(data.columns) == 4):
        eventList = read4Lines(data)
    elif (len(data.columns) == 5):
        eventList = read5Lines(data)
    else:
        myLabel = Label(mainWin, text = 'File has abnormal amount of columns. Please delete events with excess data.', pady=5, fg='red', justify='left')
        myLabel.pack()
        return

    runTime = timedelta(0) #the total time that the machine has been running on auto cycle over the data period. Only counts if it was running for more than a minute
    problemList = [] #Counts up all reasons of Cycle Interruptions

    #Collecting various data from the eventList
    for i in range(len(eventList)-1):

        #Add runtime. this is based on every cycle interruption machine event having a note of what mode it came out of and when that mode was strated. 
        #Counts up both cycle interruptions and when the machine is put into idle, both only if it was previously in auto mode for more than a minute.
        if (type(eventList[i]) == MachineEvent and eventList[i].getPrevState() == "Auto Cycling" and eventList[i].getLastDuration() >= config[0]):
            runTime += eventList[i].getLastDuration()

        #Counting up problems
        elif (type(eventList[i]) == CycleInterruptEvent and (not config[2].__contains__(eventList[i].getReason())) and (config[1] or eventList[i].getDscrp().__contains__("Inactive"))):
            problemList.append(eventList[i].getReason())
    
    #Make sets of strings to use as elements in excel file
    param = ['Start Time', 'End Time', 'Run Time (hr)', 'Availibility', 'Part Interference', 'Hopper Full', "", 'Total Cycle Interruptions']
    issues = Counter(problemList)
    amount = [eventList[-1].getTime().strftime("%m/%d/%Y %I:%M:%S %p"), eventList[0].getTime().strftime("%m/%d/%Y %I:%M:%S %p"), (round(runTime.total_seconds()/60/60, 3)), str(round(runTime / (eventList[0].getTime() - eventList[-1].getTime())*100, 2)) + "%", issues['Part Interference'], issues['Hopper Full(Metal In Conveyor)'], '', (len(problemList))]
    new_vals = issues.most_common() #Makes new counter and counts up the Cycle Interruption reasons
    new_vals = new_vals[::1] #this sorts the list in descending order
    for a, b in new_vals:
        param.append(str(a))
        amount.append(b)
        #end
    thisDict = {'Parameter': param, 'Amount': amount}
    output = pd.DataFrame(thisDict)
    output.to_excel(outputLoc + "/" + nameBox.get() + '.xlsx', index=False)

    # #Writing analytic data:
    # #Making new text file to write to
    # f = open(outputLoc + "/" + nameBox.get() + ".txt", "w")
    # #Writing total runtime
    # f.write("The total runtime over the period from " + amount[0] + " to " + amount[1] + " was " + amount[2] + " hours.\n")
    # #Writing availibility
    # f.write("Availibility: " + amount[3] + ".\n")
    # #Writing total Cycle Interruptions
    # f.write("Total Cycle Interruptions: " + amount[4] + ".\n")
    # #Writing Cycle Interruption breakdown
    # new_vals = Counter(problemList).most_common() #Makes new counter and counts up the Cycle Interruption reasons
    # new_vals = new_vals[::1] #this sorts the list in descending order
    # for a, b in new_vals:
    #     f.write(str(a) + ": " + str(b) + ", " + str(round(b/len(problemList)*100, 2)) + "%\n")
    #     #end
    # f.write("\n")
    # #Writing log to file
    # for i in range(len(eventList)-1):

    #     #Writing Machine Events to f
    #     if (type(eventList[i]) == MachineEvent):
    #         f.write(str(eventList[i]) + "\n")
        
    #     #Writing Cycle Interruptions
    #     elif (type(eventList[i]) == CycleInterruptEvent):
    #         f.write(str(eventList[i]) + "\n")
    # f.close #close file    

    #Generate message that writing is done
    myLabel = Label(mainWin, text = "Generated " + nameBox.get() + " from " + inputFile, justify='left')
    myLabel.pack()
    return
    #end analyze()