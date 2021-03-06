from Train import Train
import time
import paho.mqtt as mqtt

class Segment:
    def __init__(self,
                id,
                desc,
                length,
                nextSegment,
                nextPointPos,
                prevSegment,
                prevPointPos,
                microId,
                train,
                numCars,
                maxSpeed):

        self.id = id
        self.desc = desc
        self.length = length
        self.nextSegment = nextSegment
        self.nextPointPos = nextPointPos
        self.prevSegment = prevSegment
        self.prevPointPos = prevPointPos
        self.microId = microId
        self.train = train
        self.numCars = numCars
        self.maxSpeed = maxSpeed

# Getters and setters combined *************************************************
    def getSet_id(self, id = None):
        if id is not None:
            self.id = id
        return self.id

    def getSet_desc(self, desc = None):
        if desc is not None:
            self.desc = desc
        return self.desc

    def getSet_length(self, length = None):
        if length is not None:
            self.length = length
        return self.length

    def getSet_nextSegment(self, nextSegment = None):
        if nextSegment is not None:
            self.nextSegment = nextSegment
        return self.nextSegment

    def getSet_nextPointPos(self, nextPointPos = None):
        if nextPointPos is not None:
            self.nextPointPos = nextPointPos
        return self.nextPointPos

    def getSet_prevSegment(self, prevSegment = None):
        if prevSegment is not None:
            self.prevSegment = prevSegment
        return self.prevSegment

    def getSet_prevPointPos(self, prevPointPos = None):
        if prevPointPos is not None:
            self.prevPointPos = prevPointPos
        return self.prevPointPos

    def getSet_microId(self, microId = None):
        if microId is not None:
            self.microId = microId
        return self.microId

    def get_train(self):
        return self.train

    def set_train(self, train):
        # check if thissegment has a train
        if self.train is None:
            # check if train is an instance of Train
            if isinstance(train, Train):
                # train is valid
                self.train = train
                self.incrementNumCars()
                # send train on it's way
                self.sendTrain()
            else:
                raise Exception(self.getSet_desc + " start triggered with no train here or in prevSegment ("+self.prevSegment.getSet_desc+")")
                # print("ERROR: "+self.desc+" :train provided is not a valid Train")
        else:
            raise Exception("ERROR: segment "+self.getSet_desc + "already has a train")

    def getSet_numCars(self, numCars = None):
        if numCars is not None:
            self.numCars = numCars
        return self.numCars

    def getSet_maxSpeed(self, maxSpeed = None):
        if maxSpeed is not None:
            self.maxSpeed = maxSpeed
        return self.maxSpeed

# Methods **********************************************************************
    def processMessage(self, topic, message):
        if "segments/indicator" in topic:
            if "open" in message:
                print("Got HERE")
                print("open message received for"+topic)
                # does this segment have a train
                if self.train is None:
                    # no train currently in segment
                    # train arriving from prevSegment
                    # get the train object and set it to this segment
                    self.set_train(self.prevSegment.train)
                    # if previous segment does not have a train then this was a false trigger
                    if self.train is None:
                        # prevSegment didnot have a train
                        raise Exception(self.getSet_desc + " start triggered with no train here or in prevSegment ("+self.prevSegment.getSet_desc+")")
                    # remove car from prevSegment
                    self.prevSegment.decrementNumCars()

                else:
                    # this segment has a train
                    # is self.train moving towards next or prev segments
                    if self.train.getSet_direction() == 1:
                        None
                        # train travelling GDoT towards nextSegment
                        # remove car from prevSegment
                        # self.prevSegment.decrementNumCars()
                        # add a car to this segment
                        # self.incrementNumCars()
                    else:
                        # train is traveling !GDoT towards prevSegment
                        # does prevSegment already contain a train
                        if self.prevSegment.get_train() is None:
                            # set self.train to prevSegment
                            self.prevSegment.set_train(self.get_train())
                            self.decrementNumCars()
                        else:
                            # train already set so just move car
                            self.decrementNumCars()
                            self.prevSegment.incrementNumCars()

    def decrementNumCars(self):
        if self.numCars > 0:
            self.numCars -= 1
        if self.numCars == 0:
            self.train = None
            # track is clear for train to enter.
            # trainSent = False
            # check prevSegment for a parked train.
            if self.prevSegment.get_train() is not None:
                # there is a train here
                if self.prevSegment.get_train().getSet_speed() == 0:
                    # the train here is stopped
                    # check if trainis traveling towards this segment
                    if self.prevSegment.get_train().getSet_direction() == 1:
                        # train is heading this way so send it
                        self.prevSegment.sendTrain()

    def incrementNumCars(self):
        if self.train is None:
            print("ERROR: cannot add cars to segment with no train")
        else:
            self.numCars +=1

    def sendTrain(self):
        if self.train is None:
            print("ERROR: cannot sendTrain whe train is  None")
        else:
            if self.train.getSet_direction() == 1:
                # train is traveling GDoT to nextSegment
                # if next segment has no train then send train
                if self.nextSegment.get_train() is None:
                    # no train in nextSegment. Track is clear.
                    # send train
                    self.train.getSet_speed(self.maxSpeed)

                else:
                    # nextSegment has a train so stop.
                    self.train.getSet_speed(0)
            else:
                # train is traveling !GDoT to prevSegment
                # if next segment has no train then send train
                if self.prevSegment.get_train() is None:
                    # no train in nextSegment. Track is clear.
                    # send train
                    self.train.getSet_speed(self.maxSpeed)
                else:
                    # nextSegment has a train so stop.
                    self.train.getSet_speed(0)

    def allStop(self):
        None
        # stop all trains on all segments

    def print(self):
        print("****************trackSegment Object **********************")
        print("Id: " + str(self.id))
        print("desc: " + self.desc)
        print("microId: " + self.microId)
        if self.nextSegment is not None:
            print("Next Seg: " +str(self.nextSegment.getSet_id()))
        else:
            print("Next Seg: None")
        if(self.prevSegment is not None):
            print("Prev Seg: " +str(self.prevSegment.getSet_id()))
        else:
            print("Prev Seg: None")
        print("NumCars in segment: " + str(self.getSet_numCars()))
        if self.train is not None:
            self.train.print()
        else:
            print("Train: None")
