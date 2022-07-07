from HuskEvent import HuskEvent
from datetime import datetime
from datetime import timedelta

class CycleInterruptEvent(HuskEvent):
    """
    CycleInterruptEvent(time, type, source, description)

    A class to handle the Cycle Interruption event. Extends HuskEvent.

    This class adds the reason, activeTime, and lastDuration variables onto the standard variables of the HuskEvent class.
        reason (string): The reason for the interruption. Common reasons are part interference and hopper full (displayed as metal in conveyor in the machine output).
        activeTime (datetime): The time when the previous machine state began.
        lastDuration (timedelta): The length of time the previous machine state was active for.

    Parameters:
        time (string): The date and time of the event, which is passed on the the parent HuskEvent class. In order for the code to parse the input, the string must be of the form "YYYY-MM-DD hr:mi:se", aka the way excel handles dates and times. Also used to calculate lastDuration.
        type (string): The event type, including Access, Warning, and others.
        source (string): The source of the event, which could be a lot of things, like Clamp Piston, or the HMI Module.
        description (string): A description of the event. This is where the reason, activeTime, and lastDuration come from.

    """
    
    reason = "" #the cause of the interruption
    activeTime = None #the time that the previous state started running, a datetime object
    lastDuration = timedelta(0) #the time that the previous state was active for

    def __init__(self, dateTime, type, source, description, newFormat = False):
        HuskEvent.__init__(self, dateTime, type, source, description)
        splits = self.dscrp.split(' [', maxsplit=1)
        self.reason = splits[0]

        #Replacing metal in conveyor with the true reason
        if (self.reason == "Metal In Conveyor"):
            self.reason = "Hopper Full(Metal In Conveyor)"

        #not all cycle interruptions stop the machine. Only add activeTime and lastDuration if the interruption ends the previous state
        if(splits[1].startswith('Inactive')):
            if(newFormat):
                splits = splits[1].split('Inactive (active time was ')
                thing = splits[1].split('.')[0]
                self.activeTime = datetime.strptime(thing, "%Y-%m-%d %H:%M:%S")
                self.lastDuration = (self.time - self.activeTime)
            
            else:
                thing = splits[1].replace('Inactive (active time was ', '')
                thing = thing.replace(')]', '')
                self.activeTime = datetime.strptime(thing, "%m/%d/%Y %I:%M:%S %p")
                self.lastDuration = (self.time - self.activeTime)

    @classmethod
    def fiveLines(cls, date, time, type, source, description):
        dateTime = date + " " + time.split(".")[0]
        return cls(dateTime, type, source, description, True)

    def __str__(self):
        return "_._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._\nCycle interruption for " + self.reason + " at " + self.time.strftime("%m/%d/%Y %I:%M:%S %p")

    def setReason(self, reason):
        self.reason = reason
    
    def getReason(self):
        return self.reason
    
    def setActiveTime(self, activeTime):
        self.activeTime = activeTime

    def getActiveTime(self):
        return self.activeTime

    def setLastDuration(self, lastDuration):
        self.lastDuration = lastDuration

    def getLastDuration(self):
        return self.lastDuration
#end CycleInterruptEvent       