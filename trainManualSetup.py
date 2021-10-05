#!/usr/bin/env python3

import serial, time, sys
from cars import Car, Engine

def main():
    # create engine
    engine1 = Engine("002","ResPass 1a",40,True,True,True,("engine","passanger"),
                    "90:84:2b:01:a7:3a","/dev/ttyUSB0","0",(1,0))

    input("Connect " + engine1.name +" engine and press enter")



if __name__ == '__main__':
    main()
