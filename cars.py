import hubComs, time
class Car:
    def __init__(self,id,name,length,facing,couplingF,couplingB,types):
        self.id = id
        self.name = name
        self.length = length
        self.facing = facing
        self.couplingF = couplingF
        self.couplingB = couplingB
        self.types = types

    def get_length(self):
        return self.length

    def display_info(self):
        print("Car.id: ", self.id)
        print("Name: ", self.name)
        print("Length: ", self.length)
        print("Facing: ", self.facing)
        print("Front coupling: ", self.couplingF)
        print("Back coupling: ", self.couplingB)
        print("Types: ", self.types)

    def print(self):
        print("Car.id: ", self.id)
        print("Name: ", self.name)
        print("Length: ", self.length)
        print("Facing: ", self.facing)
        print("Front coupling: ", self.couplingF)
        print("Back coupling: ", self.couplingB)
        print("Types: ", self.types)

class Engine(Car):
    def __init__(self,id,name,length,facing,couplingF,couplingB,types,hub_add,comPort,hub_id,mFacing,maxSpeed):
        super().__init__(id,name,length,facing,couplingF,couplingB,types)
        # the bluetooth address of this hub
        self.hub_add = hub_add
        # usb port that is use to communicate to the hub
        self.comPort = comPort
        # the id number for this hub on this comPort
        self.hub_id = hub_id
        # array if ints 0,1,or -1 representing the direction that the
        # motor is facing or if motor is connected to that port at all
        # mFacing[0] is port 'A' and mFacing[1] is port 'B'
        self.mFacing = mFacing
        self.maxSpeed = maxSpeed
        self.display_info()
        self.attachHub()

    def get_maxSpeed(self):
        return self.maxSpeed

    def set_Speed(self,speed):
        # # TODO: Validation
        if speed > self.get_maxSpeed():
            speed = self.get_maxSpeed()
        print("Setting speed of ", self.name ," to ", speed)
        hubComs.sendToHub(self.comPort, "1,"+self.hub_id+","+str(speed))
        # print("{},{}".format(self.hub_id, speed).encode("utf-8"))
        # print(self.hub_id "," speed "\n")
        # ser.write("{} {}\n".format(self.hub_id, speed).encode("utf-8"))

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
        hubComs.sendToHub(self.comPort,str(self.mFacing[0])+","+str(self.mFacing[1]))
        time.sleep(0.1)

    def display_info(self):
        print("****Engine****")
        super().display_info()
        print("Hub Add: ", self.hub_add)
        print("Hub Id: ", self.hub_id)
        print("Com Port: ", self.comPort)
        print("Motors: ", self.mFacing)

    def print(self):
        print("****Engine****")
        super().print()
        print("Hub Add: ", self.hub_add)
        print("Hub Id: ", self.hub_id)
        print("Com Port: ", self.comPort)
        print("Motors: ", self.mFacing)
# ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
# ser.flush()
# car1 = Car(1,"passanger", 30, 100)
# engine1 = Engine(2,"Red PassA", 35,100,3)
#
# car1.display_info()
# engine1.display_info()
# engine1.set_Speed(20)
# time.sleep(1)
# engine1.set_Speed(0)
