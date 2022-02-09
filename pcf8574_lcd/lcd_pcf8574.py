# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Tim Hawes
#
# SPDX-License-Identifier: MIT

"""
`lcd_pcf8574`
====================================================

Module for using I2C with PCF8574 character LCD backpack

* Author(s): Kattni Rembor, Tim Hawes
"""

from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from .pcf8574 import PCF8574

# __version__ = ""
# __repo__ = ""


class Character_LCD_PCF8574(Character_LCD_Mono):
    # pylint: disable=too-few-public-methods, too-many-arguments
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of `Character_LCD_Mono` and implements all of the
    same functions and functionality.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        from lcd_pcf8574 import Character_LCD_PCF8574

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lcd = Character_LCD_PCF8574(i2c, 16, 2)
    """

    def __init__(self, i2c, columns, lines, address=None, backlight_inverted=False):
        """Initialize character LCD connected to backpack using I2C connection
        on the specified I2C bus with the specified number of columns and
        lines on the display. Optionally specify if backlight is inverted.
        """

        if address:
            pcf = PCF8574(i2c, address=address)
        else:
            pcf = PCF8574(i2c)
        pcf.switch_to_output()
        super().__init__(
            pcf.get_pin(0),
            pcf.get_pin(2),
            pcf.get_pin(4),
            pcf.get_pin(5),
            pcf.get_pin(6),
            pcf.get_pin(7),
            columns,
            lines,
            backlight_pin=pcf.get_pin(3),
            backlight_inverted=backlight_inverted,
        )
