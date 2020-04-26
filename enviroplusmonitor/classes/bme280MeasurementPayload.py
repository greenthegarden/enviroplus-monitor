from __future__ import annotations
from collections import UserDict

class Bme280MeasurementPayload(UserDict):
    """This represents a JSON object.
    """
    class TemperatureProperty(object):
        """ This class is a schema-validating wrapper around a number.
        """

        def __init__(self, value):
            self.Set(value)

        @staticmethod
        def _Validate(value):
            """Ensures that the provided number value meets all the schema constraints.
            """
            if not isinstance(value, float):
                raise ValueError("Passed value '{}' was not a number".format(value))          

        def Set(self, new_value) -> Bme280MeasurementPayload.TemperatureProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Bme280MeasurementPayload.TemperatureProperty or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()

    class HumidityProperty(object):
        """ This class is a schema-validating wrapper around a number.
        """

        def __init__(self, value):
            self.Set(value)

        @staticmethod
        def _Validate(value):
            """Ensures that the provided number value meets all the schema constraints.
            """
            if not isinstance(value, float):
                raise ValueError("Passed value '{}' was not a number".format(value))   
            if value < 0:
                raise ValueError("Value '{}' is less than the minimum of 0".format(value)) 
            if value > 100:
                raise ValueError("Value '{}' is more than the maximum of 100".format(value))      

        def Set(self, new_value) -> Bme280MeasurementPayload.HumidityProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Bme280MeasurementPayload.HumidityProperty or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()

    class PressureProperty(object):
        """ This class is a schema-validating wrapper around a number.
        """

        def __init__(self, value):
            self.Set(value)

        @staticmethod
        def _Validate(value):
            """Ensures that the provided number value meets all the schema constraints.
            """
            if not isinstance(value, float):
                raise ValueError("Passed value '{}' was not a number".format(value))          

        def Set(self, new_value) -> Bme280MeasurementPayload.PressureProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Bme280MeasurementPayload.PressureProperty or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()


    def __init__(self, data=None, **kwargs):
        """Initialization for the Bme280MeasurementPayload object.
        It can be initialized with an object, or by passing each
        object property as a keyword argument.
        """
        new_data = {}
        try:
            prop = data["temperature"] if ("temperature" in data) else kwargs["temperature"]
            if not isinstance(prop, self.TemperatureProperty):
                new_data["temperature"] = self.TemperatureProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'temperature'")
        try:
            prop = data["humidity"] if ("humidity" in data) else kwargs["humidity"]
            if not isinstance(prop, self.HumidityProperty):
                new_data["humidity"] = self.HumidityProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'humidity'")
        try:
            prop = data["pressure"] if ("pressure" in data) else kwargs["pressure"]
            if not isinstance(prop, self.PressureProperty):
                new_data["pressure"] = self.PressureProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'pressure'")
        super().__init__(new_data)

    def GetTemperature(self):
        return self.data["temperature"]
    
    def SetTemperature(self, new_value) -> Bme280MeasurementPayload:
        if not isinstance(new_value, self.TemperatureProperty):
            self.data["temperature"] = self.TemperatureProperty(new_value)
        else:
            self.data["temperature"] = new_value
        return self

    def GetHumidity(self):
        return self.data["humidity"]
    
    def SetHumidity(self, new_value) -> Bme280MeasurementPayload:
        if not isinstance(new_value, self.HumidityProperty):
            self.data["humidity"] = self.HumidityProperty(new_value)
        else:
            self.data["humidity"] = new_value
        return self

    def GetPressure(self):
        return self.data["pressure"]
    
    def SetPressure(self, new_value) -> Bme280MeasurementPayload:
        if not isinstance(new_value, self.PressureProperty):
            self.data["pressure"] = self.PressureProperty(new_value)
        else:
            self.data["pressure"] = new_value
        return self

    def Serializable(self) -> dict:
        return self.data
