class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0
        print("init")

    @property
    def voltage(self):
        print("property")
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        print("setter")
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError("{:4f} ohms must be > 0".format(ohms))
        self._ohms = ohms


class FixedResistance(Resistor):
    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, "_ohms"):
            raise AttributeError("Can't set attribute")
        self._ohms = 1




# r1 = Registor(50e3)
# r1.ohms = 10e3
# print("before r1 is {}".format(r1.ohms))
# r1.ohms += 5e3
# print("after r1 is {}".format(r1.ohms))

#
# r2 = VoltageResistance(1e3)
# print(1e3)
# print("Before : {} amps".format(r2.current))
# r2.voltage = 10
# print("After : {} amps".format(r2.current))

# r3 = BoundedResistance(1e3)
# r3.ohms = 0
# BoundedResistance(-5)

r4 = FixedResistance(1e3)
print(r4.ohms)
r4.ohms = 2e3
