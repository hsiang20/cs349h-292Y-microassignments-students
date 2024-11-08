import random
import math
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import collections as matcoll
import numpy as np

PULSE = 1
NO_PULSE = 0
OUT_NAME = "out"


class Gate:
    ID = 0

    def __init__(self, name, ports, use_id=True):
        if use_id:
            self.id = name + str(Gate.fresh_id())
        else:
            self.id = name
        self.ports = ports

    def reset(self):
        raise Exception("override me: reset state of gate <%s>" % self.id)

    def execute(self, time, inputs):
        raise Exception("override me: process input pulse and returns if the gate produces a pulse or not")

    def delay(self):
        return 1e-10

    @classmethod
    def fresh_id(cls):
        ident = Gate.ID
        Gate.ID += 1
        return ident


class LastArrival(Gate):

    def __init__(self):
        Gate.__init__(self, "LA", ["A", "B"])
        self.has_pulse = False

    def reset(self):
        # raise NotImplementedError
        self.has_pulse = False

    def execute(self, time, inputs):
        in0, in1 = inputs["A"], inputs["B"]
        # raise NotImplementedError
        if in0 == PULSE:
            if self.has_pulse:
                return PULSE
            else:
                self.has_pulse = True
        if in1 == PULSE:
            if self.has_pulse:
                return PULSE
            else:
                self.has_pulse = True
        return NO_PULSE

class FirstArrival(Gate):

    def __init__(self):
        Gate.__init__(self, "FA", ["A", "B"])
        self.has_output = False

    def reset(self):
        # raise NotImplementedError
        self.has_output = False
        return
        

    def execute(self, time, inputs):
        in0, in1 = inputs["A"], inputs["B"]
        # raise NotImplementedError
        if in0 == PULSE or in1 == PULSE:
            if not self.has_output:
                self.has_output = True
                return PULSE
        else: 
            return NO_PULSE

class Inhibition(Gate):

    def __init__(self):
        Gate.__init__(self, "INH", ["A", "B"])
        self.suppressed = False

    def reset(self):
        # raise NotImplementedError
        self.suppressed = False

    def execute(self, time, inputs):
        inA, inB = inputs["A"], inputs["B"]
        # raise NotImplementedError
        if inA:
            self.suppressed = True
        if self.suppressed: 
            return NO_PULSE
        if inB:
            return PULSE
        return NO_PULSE


class DigitalReadOutGate(Gate):

    def __init__(self):
        Gate.__init__(self, "DRO", ["A"])
        self.has_pulse = False

    def reset(self):
        raise NotImplementedError

    def delay(self):
        return 1e-10

    def execute(self, time, inputs):
        inp = inputs["A"]
        raise NotImplementedError
        return NO_PULSE


class DelayGate(Gate):

    def __init__(self, delay_ns):
        Gate.__init__(self, "DEL", ["A"])
        self.delay_ns = delay_ns
        self.pulse_time = []

    def reset(self):
        # raise NotImplementedError
        self.pulse_time = []

    def delay(self):
        return 1e-10

    def execute(self, time, inputs):
        inp = inputs["A"]
        # raise NotImplementedError
        if inp:
            self.pulse_time.append(time)
        if len(self.pulse_time) > 0:
            if (time - self.pulse_time[0]) > self.delay_ns:
                self.pulse_time = self.pulse_time[1:]
                return PULSE
        return NO_PULSE
            
        

class Input(Gate):

    def __init__(self, name):
        Gate.__init__(self, "IN.%s" % name, [], use_id=False)
        self.name = name

    def set_no_pulse(self):
        self.no_pulse = True
        self.pulse_window = (None, None)

    def set_pulse_window(self, tmin, tmax):
        self.pulse_window = (tmin, tmax)
        self.no_pulse = False

    def reset(self):
        self.generated_pulse = False
        if not self.no_pulse:
            tmin, tmax = self.pulse_window
            self.pulse_time = np.random.uniform(tmin, tmax)

    def execute(self, time, inputs):
        if self.generated_pulse or self.no_pulse:
            return NO_PULSE

        if time >= self.pulse_time:
            self.generated_pulse = True
            return PULSE

        return NO_PULSE
