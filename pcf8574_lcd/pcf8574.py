import digitalio
from adafruit_bus_device.i2c_device import I2CDevice


class DigitalInOut:
    
    def __init__(self, pin, pcf8574):
        self._pin = pin
        self._pcf8574 = pcf8574

    @property
    def direction(self):
        return self._pcf8574._direction

    @direction.setter
    def direction(self, val):
        if val is not self._pcf8574._direction:
            raise RuntimeError("Cannot change the direction of individual pin")
    
    @property
    def value(self):
        if self._pcf8574.gpio & (1 << self._pin):
            return True
        else:
            return False

    @value.setter
    def value(self, val):
        if val:
            self._pcf8574.gpio = self._pcf8574.gpio | (1 << self._pin)
        else:
            self._pcf8574.gpio = self._pcf8574.gpio & ~(1 << self._pin)

    @property
    def drive_mode(self):
        return digitalio.DriveMode.PUSH_PULL
    
    @property
    def pull(self):
        if self.direction == digitalio.Direction.OUTPUT:
            raise AttributeError
        if self._pcf8574._gpio_pull & (1 << self._pin):
            return True
        else:
            return False

    # @pull.setter
    # def pull(self, val):
    #     if self.direction == digitalio.direction.OUTPUT:
    #         raise AttributeError
    #     raise NotImplementedError

    def deinit(self):
        pass

class PCF8574:
    
    def __init__(self, i2c, address=0x27, reset=True):
        self._device = I2CDevice(i2c, address)
        self._direction = digitalio.Direction.INPUT
        self._gpio_pull = 0
        self._gpio_output = 0
        # if reset:
        #     self.gpio = 0

    def switch_to_output(self, value=0):
        self._direction = digitalio.Direction.OUTPUT
        self.gpio = value

    def switch_to_input(self):
        self._direction = digitalio.Direction.INPUT

    def _read(self):
        buf = bytearray(1)
        with self._device as device:
            device.readinto(buf)
        return buf[0]

    def _write(self, val):
        buf = bytearray([val])
        with self._device as device:
            device.write(buf)

    @property
    def gpio(self):
        if self._direction is digitalio.Direction.INPUT:
            return self._read()
        elif self._direction is digitalio.Direction.OUTPUT:
            return self._gpio_output
        else:
            raise AttributeError("Direction not set")

    @gpio.setter
    def gpio(self, val):
        if self._direction != digitalio.Direction.OUTPUT:
            raise RuntimeError("Not in output mode")
        self._gpio_output = val
        return self._write(val)

    def get_pin(self, pin):
        if not 0 <= pin <= 7:
            raise ValueError("Pin number must be 0-7.")
        return DigitalInOut(pin, self)
