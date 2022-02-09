# SPDX-FileCopyrightText: 2014 Forward Computing and Control Pty. Ltd.
# SPDX-FileCopyrightText: 2021 Tim Hawes


# 
# I2C_ClearBus
# (http://www.forward.com.au/pfod/ArduinoProgramming/I2C_ClearBus/index.html)
# (c)2014 Forward Computing and Control Pty. Ltd.
# NSW Australia, www.forward.com.au
# This code may be freely used for both private and commerical use
#
# Converted to CircuitPython by Tim Hawes.
# 


#
#  This routine turns off the I2C bus and clears it
#  on return SCA and SCL pins are tri-state inputs.
#  You need to call Wire.begin() after this to re-enable I2C
#  This routine does NOT use the Wire library at all.
# 
#  returns 0 if bus cleared
#          1 if SCL held low.
#          2 if SDA held low by slave clock stretch for > 2sec
#          3 if SDA held low after 20 clocks.
#

import digitalio
import time


def i2c_clearbus(scl_pin, sda_pin):

    scl = digitalio.DigitalInOut(scl_pin)
    sda = digitalio.DigitalInOut(sda_pin)

    # Make SDA (data) and SCL (clock) pins Inputs with pullup.
    sda.switch_to_input(pull=digitalio.Pull.UP)
    scl.switch_to_input(pull=digitalio.Pull.UP)

    # Wait 2.5 secs. This is strictly only necessary on the first power
    # up of the DS3231 module to allow it to initialize properly,
    # but is also assists in reliable programming of FioV3 boards as it gives the
    # IDE a chance to start uploaded the program
    # before existing sketch confuses the IDE by sending Serial data.
    time.sleep(2.5)

    # Check is SCL is Low.
    # If it is held low Arduno cannot become the I2C master.
    if scl.value is False:
        raise RuntimeError("SCL clock line held low")

    # > 2x9 clock
    clock_count = 20

    while sda.value is False and clock_count > 0:

        clock_count = clock_count - 1

        # Note: I2C bus is open collector so do NOT drive SCL or SDA high.
        # do not force high as slave may be holding it low for clock stretching.
        # The >5uS is so that even the slowest I2C devices are handled.
        scl.switch_to_output(value=False, drive_mode=digitalio.DriveMode.OPEN_DRAIN) # LOW
        time.sleep(0.00001) # >5uS
        scl.switch_to_input(pull=digitalio.Pull.UP) # Release/HIGH
        time.sleep(0.00001) # >5uS
    
        counter = 20

        # Check if SCL is Low.
        # loop waiting for SCL to become High only wait 2sec.
        while scl.value is False and counter > 0:
            counter = counter - 1
            time.sleep(0.1)

        if scl.value is False:
            # still low after 2 sec error
            # I2C bus error. Could not clear. SCL clock line held low by slave clock stretch for >2sec
            raise RuntimeError("SCL clock line held low by slave clock stretch")

    if sda.value is False:
        # still low
        # I2C bus error. Could not clear. SDA data line held low
        raise RuntimeError("SDA data line held low")
  
    # else pull SDA line low for Start or Repeated Start
    # When there is only one I2C master a Start or Repeat Start has the same function as a Stop and clears the bus.
    # A Repeat Start is a Start occurring after a Start with no intervening Stop.
    sda.switch_to_output(value=False, drive_mode=digitalio.DriveMode.OPEN_DRAIN) # LOW
    time.sleep(0.00001) # wait >5uS
    sda.switch_to_input(pull=digitalio.Pull.UP) # Release/HIGH
    time.sleep(0.00001) # wait >5uS

    # all ok
    sda.deinit()
    scl.deinit()
    return
