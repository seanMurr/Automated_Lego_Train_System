import Train, time

class Segment:
    def __init__(self,
                name,
                nextSegment,
                endPoint,
                prevSegment,
                startPoint,
                length,
                maxSpeed,
                train,
                segEndIndicator,
                segStartIndicator,
                mqttHost):
        self.name = name # Name of this segment
        self.nextSegment = nextSegment # TrackSegment object that comes after this
        self.endPoint = endPoint # Points object that comes before nextSegment
        self.prevSegment = prevSegment # TrackSegment object that comes before this
        self.startPoint = startPoint # Points object that comes after prevSegment
        self.length = length # length of this segment in cm
        self.maxSpeed = maxSpeed # maximum speed of this segment
        self.train = train # Train object that is currently located on this segment
        self.segEndIndicator = segEndIndicator # mqtt topic published by indicator at end of this segment
        self.segStartIndicator = segStartIndicator # mqtt topic published by indicator at start of this segment
        self.mqttHost = mqttHost # mqtt host address for publishing
        if self.train is None:
            self.segmentClear = True
        else:
            self.segmentClear = False

# Getters and setters combined *************************************************
    def getName(self, name=None):
        if name is not None:
            # set nextSegment
            self.name = name
        return self.name
    def getNextSegment(self, nextSegment=None):
        if nextSegment is not None:
            # set nextSegment
            self.nextSegment = nextSegment
        return self.nextSegment
    def getEndPoint(self, endPoint=None):
        if endPoint is not None:
            # set endPoint
            self.endPoint = endPoint
        return self.endPoint
    def getPrevSegment(self, prevSegment=None):
        if prevSegment is not None:
            # set prevSegment
            self.prevSegment = prevSegment
        return self.prevSegment
    def getStartPoint(self, startPoint=None):
        if startPoint is not None:
            # set startPoint
            self.startPoint = startPoint
        return self.startPoint
    def getLength(self, length=None):
        if length is not None:
            # set length
            self.length = length
        return self.length
    def getMaxSpeed(self, maxSpeed=None):
        if maxSpeed is not None:
            # set maxSpeed
            self.maxSpeed = maxSpeed
        return self.maxSpeed
    def getTrain(self):
        return self.train
    def setTrain(self, train=None):
        if train is not None:
            # if this segment has a train then reject new train
            if self.getTrain() is not None:
                return False
            # set train to this TrackSegment
            self.train = train
            print("Train: " + self.train.getName() + " now on segment " + self.name)
            # if next segment has train then stop train
            if self.nextSegment.getTrain() is not None:
                print("Next segment "+self.nextSegment.name+" has a train")
                print("Stopping train "+self.train.name+" on segment "+self.name)
                self.train.setSpeed(0)
            else:
                # set train speed to segment maxSpeed maintaining direction
                currentSpeed = self.train.getSpeed()
                direction = 1
                if currentSpeed != 0:
                    direction = self.train.getSpeed()/abs(self.train.getSpeed())
                self.train.setSpeed(self.maxSpeed * direction)
            return True

    def getSegEndIndicator(self, segEndIndicator=None):
        if segEndIndicator is not None:
            # set segEndIndicator to this TrackSegment
            self.segEndIndicator = segEndIndicator
        return self.segEndIndicator
    def getSegStartIndicator(self, segStartIndicator = None):
        if segStartIndicator is not None:
            # set segStartIndicator to this TrackSegment
            self.segStartIndicator = segStartIndicator
        return self.segStartIndicator

# Methods **********************************************************************
    def activateSegEndIndicator(self,msg):
        # msg will be either "open" or "closed"
        msg = msg.decode('utf-8')
        if str(msg)  == "open":
            print("segment "+self.name+" received 'open'")
            # if a train is present and is moving then train is leaving this segment
            if (self.train is not None):
                print("there is a train leaving this segment, give train to next segment")
                if self.nextSegment.setTrain(self.train):
                    print(self.train.name + " passsed to segment "+self.nextSegment.name)
                    self.train = None
                else:
                    # train was not accepted by nextSegment.
                    print("ERROR: "+self.nextSegment.name + " already has train: "+self.nextSegment.train.name)
                    print("TO-DO: recalling "+self.train.name)
                    # # Stop train
                    # trainDir = self.train.getSpeed()
                    # trainDir = trainDir/abs(trainDir)
                    # self.train.setSpeed(0)
                    # # backup for 1 sec
                    # self.train.setSpeed(80*trainDir)
                    # time.sleep(1)
                    # self.train.setSpeed(0)
                    # # don't call next train
                    # self.segmentClear = False
            else:
                print("Segment "+self.name+" does not have a train")

            # tell previous segment that this segment is clear if this segment has no train
            if self.train is None:
                print("telling segment "+self.prevSegment.name + " to send train")
                self.prevSegment.sendTrain()
            else:
                print("Segment "+self.name+" still has train "+self.train.name)

    def sendTrain(self):
        print("segment " +self.name+ " sending train")
        # if there is a train on this segment
        if self.train is not None:
            print("segment " +self.name+ " has train " + self.train.getName())
            # check if nextSegment is clear
            if self.nextSegment.getTrain() is None:
                print("path is clear to send train")
                # if train is stopped
                # print(self.train.getName() + " has speed of " +str(self.train.getSpeed()))
                if self.train.getSpeed() == 0:
                    print("starting "+self.train.getName())
                    # start train
                    self.train.setSpeed(self.maxSpeed)
        else:
            print("segment " +self.name+ " has no train to send")

    def print(self):
        # output this segment to terminal
        print("Track Segment Object")
        print("Name: " + self.name)
        if(self.nextSegment is not None):
            print("Next Seg: "+ self.nextSegment.getName())
        else:
            print("Next Seg: None")
        if(self.nextSegment is not None):
            print("Prev Seg: "+ self.prevSegment.getName())
        else:
            print("Prev Seg: None")
        if(self.endPoint is not None):
            print("End Points: "+ self.endPoint)
        else:
            print("End Points: None")
        if(self.startPoint is not None):
            print("Start Points: "+ self.startPoint)
        else:
            print("Start Points: None")
        print("Length: " + str(self.length))
        if(self.segEndIndicator is not None):
            print("Segment end indicator: "+ self.segEndIndicator)
        else:
            print("Segment end indicator: None")
        if(self.segStartIndicator is not None):
            print("Segment start indicator: "+ self.segStartIndicator)
        else:
            print("Segment start indicator: None")
        if(self.train is not None):
            self.train.print()
        else:
            print("Train: None")
        print("mqtt Server: " + str(self.mqttHost))
