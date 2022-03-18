from Train import Train
import time
import paho.mqtt as mqtt

class Segment:
    def __init__(self,
                id,
                desc,
                length,
                nextSegment,
                nextPointAddress,
                nextPointValues,
                nextPointPos,
                prevSegment,
                prevPointAddress,
                prevPointValues,
                prevPointPos,
                microId,
                train,
                numCars,
                maxSpeed):

        self.id = id
        self.desc = desc
        self.length = length
        self.nextSegment = nextSegment
        self.nextPointAddress = nextPointAddress
        self.nextPointValues = nextPointValues
        self.nextPointPos = nextPointPos
        self.prevSegment = prevSegment
        self.prevPointAddress = prevPointAddress
        self.prevPointValues = prevPointValues
        self.prevPointPos = prevPointPos
        self.microId = microId
        self.train = train
        self.numCars = numCars
        self.maxSpeed = maxSpeed
        self.set_nextPoint(nextPointPos)
        self.set_prevPoint(prevPointPos)
        self.siblingSegment = None

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

    def getSet_siblingSegment(self, siblingSegment = None):
        if siblingSegment is not None:
            self.siblingSegment = siblingSegment
        return self.siblingSegment

    def get_nextSegment(self):
        return self.nextSegment[self.getSet_nextPointPos()]

    def getSet_nextPointPos(self, nextPointPos = None):
        if nextPointPos is not None:
            self.nextPointPos = nextPointPos
            set_nextPoint(self.nextPointPos)
        return self.nextPointPos

    def get_prevSegment(self):
        return self.prevSegment[self.getSet_prevPointPos()]

    def getSet_prevPointPos(self, prevPointPos = None):
        if prevPointPos is not None:
            self.prevPointPos = prevPointPos
            set_nextPoint(self.prevPointPos)
        return self.prevPointPos

    def getSet_microId(self, microId = None):
        if microId is not None:
            self.microId = microId
        return self.microId

    def get_train(self):
        if self.train is None:
            if self.getSet_siblingSegment() is not None:
                return self.getSet_siblingSegment().train
        return self.train

    def set_train(self, train):
        # check if this segment has a train
        if self.train is None:
            # check if train is an instance of Train
            if isinstance(train, Train):
                # train is valid
                self.train = train
                self.incrementNumCars()
                # self.get_prevSegment().decrementNumCars()
                # send train on it's way
                self.sendTrain()
            else:
                raise Exception(self.getSet_desc + " start triggered with no train here or in prevSegment ("+self.get_prevSegment().getSet_desc+")")
                # print("ERROR: "+self.desc+" :train provided is not a valid Train")
        else:
            raise Exception("ERROR: segment "+self.getSet_desc() + "already has a train")

    def getSet_numCars(self, numCars = None):
        if numCars is not None:
            self.numCars = numCars
        return self.numCars

    def getSet_maxSpeed(self, maxSpeed = None):
        if maxSpeed is not None:
            self.maxSpeed = maxSpeed
        return self.maxSpeed

    def set_nextSegment(self, segment, pointValue):
        # if fist segment in list is None then set this segment as first in list
        if self.nextSegment[0] is None:
            self.nextSegment[0] = segment
            self.nextPointValues[0] = pointValue
        else:
            self.nextSegment.append(segment)
            self.nextPointValues.append(pointValue)

    def set_prevSegment(self, segment, pointValue):
        # if fist segment in list is None then set this segment as first in list
        if self.prevSegment[0] is None:
            self.prevSegment[0] = segment
            self.prevPointValues[0] = pointValue
        else:
            self.prevSegment.append(segment)
            self.prevPointValues.append(pointValue)


# Methods **********************************************************************
    def set_nextPoint(self,nextPointPos):
        if len(self.nextSegment) == 1:
            # there is only 1 segment
            return
        elif len(self.nextSegment) == 0:
            # no segments yet attached
            return
        print("TODO: SEND MQTT TOPIC: " + str(self.nextPointAddress) + " MESSAGE: " + str(self.nextPointValues[nextPointPos]))

    def set_prevPoint(self,prevPointPos):
        if len(self.prevSegment) == 1:
            # there is only 1 segment
            return
        elif len(self.prevSegment) == 0:
            # no segments yet attached
            return
        print("SEND MQTT TOPIC: " + self.prevPointAddress + " MESSAGE: " + self.prevPointValues[nextPointPos])

    def processMessage(self, topic, message):
        if "segments/indicator" in topic:
            if True:
                print("Got HERE")
                print("train has triggered end of segment "+str(self.id))
                # does this segment have a train
                if self.get_train() is None:
                    print("no train currently in segment")
                    # train must have passed prev segment undetected
                    if self.get_prevSegment().get_train() is None:
                        # train has passed multiple segments undetected.
                        raise Exception(self.getSet_desc + " train has passed multiple segments undetected ")
                    else:
                        self.set_train(self.get_prevSegment().get_train())
                        self.processMessage(topic,message)

                    # train arriving from nextSegment (!GDOT)
                    # TODO:


                else:
                    print("this segment has a train")
                    # train is moving to nextSegment (GDOT)
                    # Does nextSegment have a train
                    if self.get_nextSegment().get_train() is None:
                        print("next segment does not have a train")
                        self.get_nextSegment().set_train(self.get_train())
                        self.decrementNumCars()
                        # check if train has/should have left previous segment
                        print("processMessage(): make sure train has left prev segments")
                        seg = self
                        segLength = 0
                        print("getting train length "+str(self.id))
                        trainLength = self.get_train().get_length()
                        print("comparing length of train to length of segments")
                        while trainLength > segLength:
                            segLength += seg.getSet_length()
                            seg = seg.get_prevSegment()

                        # make sure self.train has been removed from seg
                        print("make sure train has been removed from segment "+str(seg.id))
                        if seg.get_train() is self.get_train():
                            # remove cars from previous segment
                            print("removing cars from segment "+str(seg.id))
                            for car in range(seg.getSet_numCars()):
                                seg.decrementNumCars()
                        else:
                            print("train already removed from segment "+str(seg.id))

                    else:
                        print("next segment has a train")
                        # is nextSegment's train this train
                        if self.get_nextSegment().get_train() is self.get_train():
                            print("same train")
                            # train is in the process of moving from this segment to nextSegment
                            self.get_nextSegment().incrementNumCars()
                            self.decrementNumCars()
                        else:
                            # there is another train currently in nextSegment
                            # ERROR: possible collision detected
                            # print("ERROR: Collision detection in segment " + self.get_nextSegment().getSet_desc())
                            # print("Train moving from segment "+self.getSet_desc())
                            # print("Stopping ALL trains")
                            # raise Exception("ERROR: Collision Detected. Stopping ALL trains")
                            if self.get_nextSegment().getSet_siblingSegment() is not None:
                                print("train is in next segments sibling segment")
                                # send train car to next segment
                                print("set train (" + self.train.cars[0].name + ") to next segment (" +self.get_nextSegment().desc +")")
                                self.get_nextSegment().set_train(self.train)
                                # stop train
                                print("STOP train ("+self.train.cars[0].name+")")
                                self.train.getSet_speed(0)
                                print("Decrement car from ("+self.desc+")")
                                self.decrementNumCars()
            self.shortPrint()



                    # if self.train.getSet_direction() == 1:
                    #     None
                    #     # train travelling GDoT towards nextSegment
                    #     # remove car from prevSegment
                    #     # self.prevSegment.decrementNumCars()
                    #     # add a car to this segment
                    #     # self.incrementNumCars()
                    # else:
                    #     # train is traveling !GDoT towards prevSegment
                    #     # does prevSegment already contain a train
                    #     if self.prevSegment.get_train() is None:
                    #         # set self.train to prevSegment
                    #         self.prevSegment.set_train(self.get_train())
                    #         self.decrementNumCars()
                    #     else:
                    #         # train already set so just move car
                    #         self.decrementNumCars()
                    #         self.prevSegment.incrementNumCars()

    def decrementNumCars(self):
        if self.numCars > 0:
            self.numCars -= 1
        print("segment: " + self.getSet_desc() + " has " +str(self.getSet_numCars()) )
        if self.numCars == 0:
            # check if prevSegment still contains this train
            if self.get_prevSegment().train is self.train:
                self.numCars = self.get_prevSegment().numCars
                while self.get_prevSegment().numCars > 0:
                    self.get_prevSegment().decrementNumCars()
            else:
                self.train = None
                print("track is clear for train to enter.")
                self.get_prevSegment().sendTrain()
                if self.getSet_siblingSegment() is not None:
                    self.getSet_siblingSegment().get_prevSegment().sendTrain()
                # trainSent = False
                # check prevSegment for a parked train.
                # self.get_prevSegment().sendTrain()
                if self.get_prevSegment().get_train() is not None:
                    print("there is a train here")
                    if self.get_prevSegment().get_train().getSet_speed() == 0:
                        print("the train here is stopped")
                        # check if train is traveling towards this segment
                        if self.get_prevSegment().get_train().getSet_direction() == 1:
                            print("train is heading this way so send it")
                            self.get_prevSegment().sendTrain()

    def incrementNumCars(self):
        if self.train is None:
            print("ERROR: cannot add cars to segment with no train")
        else:
            self.numCars +=1

    def sendTrain(self, count = 0):
        print("sendTrain(" + self.getSet_desc() + ")")
        if self.train is None:
            if count < 20:
                print("No train in " + self.getSet_desc() + ". Trying " + self.get_prevSegment().getSet_desc())
                self.get_prevSegment().sendTrain(count)
        else:
            print("has train")
            if self.get_train().getSet_direction() == 1:
                print("train is travelling GDoT")
                # train is traveling GDoT to nextSegment
                # if next segment has no train then send train
                if self.get_nextSegment().get_train() is None:
                    # no train in nextSegment. Track is clear.
                    print("no train in " + self.get_nextSegment().getSet_desc())
                    # send train
                    print("setting train "+self.get_train().cars[0].name+" speed to "+str(self.maxSpeed)+" maximum")
                    self.get_train().getSet_speed(self.maxSpeed)

                else:
                    print("nextSegment has a train so stop")
                    self.get_train().getSet_speed(0)
                    print("Trying " + self.get_prevSegment().getSet_desc())
                    self.get_prevSegment().sendTrain()

            else:
                # train is traveling !GDoT to prevSegment
                # if next segment has no train then send train
                if self.get_prevSegment().get_train() is None:
                    # no train in nextSegment. Track is clear.
                    # send train
                    self.get_train().getSet_speed(self.maxSpeed)
                else:
                    # nextSegment has a train so stop.
                    self.get_train().getSet_speed(0)


    def allStop(self):
        None
        # stop all trains on all segments

    def shortPrint(self):
        seg = self
        # find segment[0]
        print("looking for segment[0]")
        while seg.getSet_id() != 0:
            seg = seg.get_nextSegment()
        print("segment[0] found")
        # cycle through each nextSegment. print segment name and train
        self.shortPrintMessage(seg)
        seg = seg.get_nextSegment()
        while seg.getSet_id() != 0:
            self.shortPrintMessage(seg)
            seg = seg.get_nextSegment()
    def shortPrintMessage(self, seg):
        message = seg.desc
        sibId = "  "
        if seg.siblingSegment is not None:
            id = seg.getSet_siblingSegment().getSet_id()
            # print("sibling " + str(id) + " found")
            sibId = ""
            if id < 10:
                sibId = "0"
            sibId += str(id)
            # print("sibling " + sibId + " found")
        message += " " + sibId
        if seg.train is not None:
            message += " " + seg.train.cars[0].name + " " +str(seg.train.speed)
        print(message)

    def print(self):
        print("****************trackSegment Object **********************")
        print("Id: " + str(self.id))
        print("desc: " + self.desc)
        print("microId: " + self.microId)
        if self.get_nextSegment() is not None:
            print("Next Seg: " +str(self.get_nextSegment().getSet_id()) + "  Pos: " + str(self.get_nextSegment().nextPointValues[self.get_nextSegment().nextPointPos]))
        else:
            print("Next Seg: None")
        if(self.get_prevSegment() is not None):
            print("Prev Seg: " +str(self.get_prevSegment().getSet_id()) + "  Pos: " + str(self.get_prevSegment().prevPointValues[self.get_prevSegment().prevPointPos]))
        else:
            print("Prev Seg: None")
        print("NumCars in segment: " + str(self.getSet_numCars()))
        if self.train is not None:
            self.train.print()
        else:
            print("Train: None")
