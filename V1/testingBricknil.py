from curio import sleep
from bricknil import attach, start
from bricknil.hub import PoweredUpHub
from bricknil.sensor import TrainMotor

@attach(TrainMotor, name='motor_A')
@attach(TrainMotor, name='motor_B')
class Train(PoweredUpHub):

    async def run(self):
        for i in range(2):  # Repeat this control two times
            await self.motor_A.ramp_speed(30,5000) # Ramp speed to 80 over 5 seconds
            await self.motor_B.ramp_speed(30,5000) # Ramp speed to 80 over 5 seconds
            await sleep(6)
            await self.motor_A.ramp_speed(0,1000)  # Brake to 0 over 1 second
            await self.motor_B.ramp_speed(0,1000)  # Brake to 0 over 1 second
            await sleep(2)

async def system():
    # train = Train('My train', ble_id='90:84:2b:21:db:7d')
    train = Train('My train')

if __name__ == '__main__':
    start(system)
