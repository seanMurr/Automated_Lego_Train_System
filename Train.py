from cars import Car, Engine

class Train:
    def __init__(self,cars,speed,direction):
        self.cars = cars
        self.speed = speed
        self.direction = direction
        self.timeStopped = None

# Getters and setters combined *************************************************
    def getSet_direction(self, direction = None):
        if direction is not None:
            self.direction = direction
        return self.direction

    def getSet_speed(self, speed = None):
        if speed is not None:
            self.speed = speed
            # send speed to each engine in train
            for car in self.cars:
                if isinstance(car,Engine):
                    # this car is an Engine
                    car.set_Speed(self.speed)
            if speed != 0:
                self.timeStopped = None
            else:
                None
                # TODO: set the timeStopped value to now
        return self.speed

    def get_length(self):
        length = 0
        for car in self.cars:
            length += car.get_length()
        return length

# Methods **********************************************************************
    def print(self):
        print("Train Object")
        print("Speed: "+str(self.speed))
        print("Direction: "+str(self.direction))
        print("Cars")
        print("Num cars: "+ str(len(self.cars)))
        for car in self.cars:
            car.print()
