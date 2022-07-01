from datetime import datetime

class HuskEvent:
    """
    HuskEvent(time, type, source, description)

    An abstract class to handle the inputs that come directly from the machine data sheet.
    
    Each row of the ouput from the machine has a line for date and time, event type, source, and a desfription. Each of these 4 things is contained by this class.

    Parameters: 
        time (string): The date and time of the event, which is converted to a datetime object during initialization. In order for the code to parse the input, the string must be of the form "YYYY-MM-DD hr:mi:se", aka the way excel handles dates and times.
        type (string): The event type, including Access, Warning, and others.
        source (string): The source of the event, which could be a lot of things, like Clamp Piston, or the HMI Module.
        description (string): A description of the event. The form of this changes for each event, and usually this is further analyzed by any child classes.
    
    """

    time = None #The time of day, denoted as a datetime object
    type = "" #The type of event, such as Cycle Interruption, Access, or Warning
    sorc = "" #The source of the event
    dscrp = "" #The full descrption of the event. This is often broken down further by inheriting clases

    def __init__(self, time, type, source, description):
        self.type = type
        self.time = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
        self.sorc = source
        self.dscrp = description

    def __str__(self) -> str:
        pass
    
    def setType(self, type):
        self.type = type
    
    def getType(self):
        return self.type

    def setTime(self, time):
        self.time = time

    def getTime(self):
        return self.time

    def setSorc(self, sorc):
        self.sorc = sorc
    
    def getSorc(self):
        return self.sorc

    def setDscrp(self,dscrp):
        self.dscrp = dscrp
    
    def getDscrp(self):
        return self.dscrp
