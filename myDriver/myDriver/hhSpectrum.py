#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install pyVisa
import visa
from traceback import format_exc


class Spectrum(object):
    def __init__(self, addr=18):
        self.__addr = addr
        self.__open = False
        self.__resource = None
        self.__device = None

    def open(self):
        try:
            # GPIB Configuration
            self.__resource = visa.ResourceManager()
            self.__device = self.__resource.open_resource('GPIB0::{}::INSTR'.format(self.__addr))
            self.__open = True
        except Exception as e:
            self.__open = False
            print('{}\n{}'.format(e, format_exc()))
        return self.__open

    def config(self, freq, span, level):
        if not self.open():
            return False
        try:
            self.__device.write("*RST")  # reset the instrument, default 401 meas points
            # Instrument Initialisation
            self.__device.write("INIT:CONT 0")  # Single sweep mode, manual trigger
            self.__device.write("INIT:IMM;*WAI")  # Perform a single sweep (recomended practice)
            # RF Configuration
            self.__device.write("FREQ:CENT %d Hz" % freq)  # Set the RF Centre Frequency
            self.__device.write("FREQ:SPAN %d Hz" % span)
            self.__device.write("DISP:WIND:TRAC:Y:SCAL:RLEV %f dBm" % level)  # Set the analyser reference level
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def measure(self):
        if not self.open():
            return None
        try:
            self.__device.write("INIT:IMM;*WAI")  # Perform the measurement sweep itself
            # Result Recovery
            self.__device.write("TRAC:DATA? TRACE1")  # Request amplitude (dBm) trace data
            traceData = self.__device.read()
            self.__device.write("CALC:MARK:MAX")  # Request marker Peak Search
            self.__device.write("CALC:MARK:X?")  # Recover marker frequency
            maxFrequency = self.__device.read()
            self.__device.write("CALC:MARK:Y?")  # Recover marker amplitude
            maxAmplitude = self.__device.read()
            return traceData, maxFrequency, maxAmplitude  # Dictionary of all results
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return None


if __name__ == '__main__':
    s = Spectrum(18)
    s.config(470e6, 1e6, 35)
    rep = s.measure()
    if rep:
        print(rep)
        data, freq, power = rep
