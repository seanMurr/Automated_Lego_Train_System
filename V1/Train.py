import hubComs, time

class Train:
    # initialise the train object variables and send details to the controller
    # to enable attaching to the hub
    def __init__(self, name, length, speed, maxSpeed, hub_add,comPort,hub_id,motors):
        self.name = name
        self.length = length
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.hub_add = hub_add
        self.comPort = comPort
        self.hub_id = hub_id
        self.motors = motors
        self.attachHub()

# Getters and setters combined *************************************************
    def getName(self, name = None):
        if name is not None:
            # set name
            self.name = name
        return self.name

    def getLength(self, length = None):
        if length is not None:
            # set length
            self.length = length
        return self.length

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        # set speed
        print("setting speed of "+self.name+" to "+str(speed))
        if speed > self.maxSpeed:
            direction = speed / abs(speed)
            speed = self.maxSpeed * direction
        self.speed = speed
        hubComs.sendToHub(self.comPort, "1,"+self.hub_id+","+str(speed))

    def getMaxSpeed(self, maxSpeed = None):
        if maxSpeed is not None:
            # set maxSpeed
            self.maxSpeed = maxSpeed
        return self.maxSpeed

# Methods **********************************************************************
    def attachHub(self):
        # put bluetooth device into setup mode
        hubComs.sendToHub(self.comPort,"0")
        time.sleep(0.1)
        # send the id of this hub on this port
        hubComs.sendToHub(self.comPort,self.hub_id)
        time.sleep(0.1)
        # send the bluetooth address for this hub
        hubComs.sendToHub(self.comPort,self.hub_add)
        time.sleep(0.1)
        # send name of engine
        hubComs.sendToHub(self.comPort,self.name)
        time.sleep(0.1)
        # send motor directions
        hubComs.sendToHub(self.comPort,str(self.motors[0])+","+str(self.motors[1]))
        time.sleep(0.1)

    def print(self):
        # output status of the train object to terminal
        print("Train Object")
        print("Name: " + self.name)
