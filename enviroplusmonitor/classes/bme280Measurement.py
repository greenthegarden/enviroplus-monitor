from __future__ import annotations
from collections import UserDict
from collections import UserList

class Bme280Measurement(UserDict):
    """This represents a JSON object.
    """
    class SensorProperty(object):
        """ This class is a schema-validating wrapper around a string.
        """

        def __init__(self, value="BME280"):
            self.Set(value)

        @staticmethod
        def _Validate(value):
            """Ensures that the provided string value meets all the schema constraints.
            """
            if not isinstance(value, str):
                raise ValueError("Passed value '{}' was not a string".format(value))          

        def Set(self, new_value) -> Bme280Measurement.SensorProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a Bme280Measurement.SensorProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class MeasurementsProperty (UserList):
        """ This represents a JSON array.
        """
        
        
        def __init__(self, the_list=None):
            """Initializer for array.
            """
            if not hasattr(the_list, '__iter__'):
                raise TypeError("The provided list was not iterable")

            self.the_list = the_list

            if isinstance(the_list, type(self)):
                super().__init__(the_list.data)
            else:
                super().__init__([self.Item(x) for x in the_list])

        def Append(self, new_value) -> MeasurementsProperty:
            self.data.append(self.Item(new_value))
            return self

        def Serializable(self) -> list:
            return self.data


    def __init__(self, data=None, **kwargs):
        """Initialization for the Bme280Measurement object.
        It can be initialized with an object, or by passing each
        object property as a keyword argument.
        """
        new_data = {}
        try:
            prop = data["sensor"] if ("sensor" in data) else kwargs["sensor"]
            if not isinstance(prop, self.SensorProperty):
                new_data["sensor"] = self.SensorProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["measurements"] if ("measurements" in data) else kwargs["measurements"]
            if not isinstance(prop, self.MeasurementsProperty):
                new_data["measurements"] = self.MeasurementsProperty(prop)
        except KeyError:
            pass
        super().__init__(new_data)

    def GetSensor(self):
        return self.data["sensor"]
    
    def SetSensor(self, new_value) -> Bme280Measurement:
        if not isinstance(new_value, self.SensorProperty):
            self.data["sensor"] = self.SensorProperty(new_value)
        else:
            self.data["sensor"] = new_value
        return self

    def GetMeasurements(self):
        return self.data["measurements"]
    
    def SetMeasurements(self, new_value) -> Bme280Measurement:
        if not isinstance(new_value, self.MeasurementsProperty):
            self.data["measurements"] = self.MeasurementsProperty(new_value)
        else:
            self.data["measurements"] = new_value
        return self

    def Serializable(self) -> dict:
        return self.data
