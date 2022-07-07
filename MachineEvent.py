from datetime import datetime
from datetime import timedelta
from HuskEvent import HuskEvent

class MachineEvent(HuskEvent):
    """
    MachineEvent(time, type, source, description)

    A class to handle the different Machine state events. Extends HuskEvent.

    This class adds the state, prevState, stepTime, and lastDuration variables onto the standard variables of the HuskEvent class.
        state (string): The new state of the machine. Auto Cycling, Cycle Interruption, and Idle/Manual are common.
        prevState (string): The previos state of the machine.
        stepTime (datetime): The time that the previous state started running.
        lastDuration (timedelta): The length of time the previous machine state was active for.

    Parameters:
        time (string): The date and time of the event, which is passed on the the parent HuskEvent class. In order for the code to parse the input, the string must be of the form "YYYY-MM-DD hr:mi:se", aka the way excel handles dates and times. Also used to calculate lastDuration.
        type (string): The event type, including Access, Warning, and others.
        source (string): The source of the event, which could be a lot of things, like Clamp Piston, or the HMI Module.
        description (string): A description of the event. This is where the state, prevState, stepTime, and lastDuration come from.

    """
    
    state = "" #the state that the machine is put into
    prevState = "" #the previous state the machine was in
    stepTime = None #the time that the previous state started running, a datetime object
    lastDuration = timedelta(0) #the time that the previous state was active for

    def __init__(self, dateTime, type, source, description, newFormat = False):
        HuskEvent.__init__(self, dateTime, type, source, description)
        #handles init differently if the machine was off
        if (self.dscrp.startswith(" Initial State")):
            self.state = "Idle/Manual"
            self.prevState = "Off"
            return

        splits = self.dscrp.split(' from  ', maxsplit=1)
        self.state = splits[0]
        splits = splits[1].split(' (started ', maxsplit=1)
        self.prevState = splits[0]
        
        if(newFormat):
            splits = splits[1].split('.')
            self.stepTime = datetime.strptime(splits[0], "%Y-%m-%d %H:%M:%S")
        else:
            splits = splits[1].split(')')
            self.stepTime = datetime.strptime(splits[0], "%m/%d/%Y %I:%M:%S %p")
        self.lastDuration = self.time - self.stepTime
        

    @classmethod
    def fiveLines(cls, date, time, type, source, description):
        dateTime = date + " " + time.split(".")[0]
        return cls(dateTime, type, source, description, True)


    def __str__(self) -> str:
        #handles str differently if the machine was off
        if self.prevState != "Off":
            return "__________________________________________________________________________________________________________________\nNew state: " + self.state + " as of " + self.time.strftime("%m/%d/%Y %I:%M:%S %p") + "\nPrevious State: " + self.prevState + " as of " + self.stepTime.strftime("%m/%d/%Y %I:%M:%S %p") +  "\nTime Since Last State Change: " + timedelta.__str__(self.lastDuration)
        #standard str
        else:
            return "__________________________________________________________________________________________________________________\nNew state: " + self.state + " as of " + self.time.strftime("%m/%d/%Y %I:%M:%S %p") + "\nPrevious State: " + self.prevState

    def setState(self, state):
        self.state = state
    
    def getState(self):
        return self.state
    
    def setPrevState(self, prevState):
        self.prevState = prevState
    
    def getPrevState(self):
        return self.prevState
    
    def setStepTime(self, stepTime):
        self.stepTime = stepTime

    def getStepTime(self):
        return self.stepTime

    def setLastDuration(self, lastDuration):
        self.lastDuration = lastDuration

    def getLastDuration(self):
        return self.lastDuration
    
    def setReason(self, reason):
        self.reason = reason

    def getReason(self):
        return self.reason

