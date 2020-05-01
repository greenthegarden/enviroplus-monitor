from __future__ import annotations
from collections import UserDict

class Mics6814MeasurementPayload(UserDict):
    """This represents a JSON object.
    """
    class OxidisingProperty(object):
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

        def Set(self, new_value) -> Mics6814MeasurementPayload.OxidisingProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Mics6814MeasurementPayload.OxidisingProperty or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()

    class ReducingProperty(object):
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

        def Set(self, new_value) -> Mics6814MeasurementPayload.ReducingProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Mics6814MeasurementPayload.ReducingProperty or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()

    class Nh3Property(object):
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

        def Set(self, new_value) -> Mics6814MeasurementPayload.Nh3Property:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Mics6814MeasurementPayload.Nh3Property or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()


    def __init__(self, data=None, **kwargs):
        """Initialization for the Mics6814MeasurementPayload object.
        It can be initialized with an object, or by passing each
        object property as a keyword argument.
        """
        new_data = {}
        try:
            prop = data["oxidising"] if ("oxidising" in data) else kwargs["oxidising"]
            if not isinstance(prop, self.OxidisingProperty):
                new_data["oxidising"] = self.OxidisingProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'oxidising'")
        try:
            prop = data["reducing"] if ("reducing" in data) else kwargs["reducing"]
            if not isinstance(prop, self.ReducingProperty):
                new_data["reducing"] = self.ReducingProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'reducing'")
        try:
            prop = data["nh3"] if ("nh3" in data) else kwargs["nh3"]
            if not isinstance(prop, self.Nh3Property):
                new_data["nh3"] = self.Nh3Property(prop)
        except KeyError:
            raise ValueError("Missing property 'nh3'")
        super().__init__(new_data)

    def GetOxidising(self):
        return self.data["oxidising"]
    
    def SetOxidising(self, new_value) -> Mics6814MeasurementPayload:
        if not isinstance(new_value, self.OxidisingProperty):
            self.data["oxidising"] = self.OxidisingProperty(new_value)
        else:
            self.data["oxidising"] = new_value
        return self

    def GetReducing(self):
        return self.data["reducing"]
    
    def SetReducing(self, new_value) -> Mics6814MeasurementPayload:
        if not isinstance(new_value, self.ReducingProperty):
            self.data["reducing"] = self.ReducingProperty(new_value)
        else:
            self.data["reducing"] = new_value
        return self

    def GetNh3(self):
        return self.data["nh3"]
    
    def SetNh3(self, new_value) -> Mics6814MeasurementPayload:
        if not isinstance(new_value, self.Nh3Property):
            self.data["nh3"] = self.Nh3Property(new_value)
        else:
            self.data["nh3"] = new_value
        return self

    def Serializable(self) -> dict:
        return self.data
