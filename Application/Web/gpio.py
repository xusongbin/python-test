#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO


class Led(object):
    def __init__(self):
        self.led_pin = 36
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def set(self, sta):
        if sta.upper() == 'ON':
            GPIO.output(self.led_pin, True)
        else:
            GPIO.output(self.led_pin, False)


