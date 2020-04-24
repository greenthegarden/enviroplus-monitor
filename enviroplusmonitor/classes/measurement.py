from __future__ import annotations
from collections import UserDict

class Measurement(UserDict):
    """This represents a JSON object.
    """
    class LabelProperty(object):
        """ This class is a schema-validating wrapper around a string.
        """

        def __init__(self, value):
            self.Set(value)

        @staticmethod
        def _Validate(value):
            """Ensures that the provided string value meets all the schema constraints.
            """
            if not isinstance(value, str):
                raise ValueError("Passed value '{}' was not a string".format(value))          

        def Set(self, new_value) -> Measurement.LabelProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a Measurement.LabelProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class ValueProperty(object):
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

        def Set(self, new_value) -> Measurement.ValueProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, float):
                self._Validate(new_value)
                self._value = new_value
            elif isinstance(new_value, int):
                self._Validate(float(new_value))
                self._value = float(new_value)
            else:
                raise TypeError("The provided type was not a Measurement.ValueProperty or a float")
            return self

        def Get(self) -> float:
            return self._value

        def Serializable(self) -> float:
            return self.Get()

    class UnitsProperty(object):
        """ This class is a schema-validating wrapper around a string.
        """

        def __init__(self, value):
            self.Set(value)

        @staticmethod
        def _Validate(value):
            """Ensures that the provided string value meets all the schema constraints.
            """
            if not isinstance(value, str):
                raise ValueError("Passed value '{}' was not a string".format(value))          

        def Set(self, new_value) -> Measurement.UnitsProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a Measurement.UnitsProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()


    def __init__(self, data=None, **kwargs):
        """Initialization for the Measurement object.
        It can be initialized with an object, or by passing each
        object property as a keyword argument.
        """
        new_data = {}
        try:
            prop = data["label"] if ("label" in data) else kwargs["label"]
            if not isinstance(prop, self.LabelProperty):
                new_data["label"] = self.LabelProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["value"] if ("value" in data) else kwargs["value"]
            if not isinstance(prop, self.ValueProperty):
                new_data["value"] = self.ValueProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["units"] if ("units" in data) else kwargs["units"]
            if not isinstance(prop, self.UnitsProperty):
                new_data["units"] = self.UnitsProperty(prop)
        except KeyError:
            pass
        super().__init__(new_data)

    def GetLabel(self):
        return self.data["label"]
    
    def SetLabel(self, new_value) -> Measurement:
        if not isinstance(new_value, self.LabelProperty):
            self.data["label"] = self.LabelProperty(new_value)
        else:
            self.data["label"] = new_value
        return self

    def GetValue(self):
        return self.data["value"]
    
    def SetValue(self, new_value) -> Measurement:
        if not isinstance(new_value, self.ValueProperty):
            self.data["value"] = self.ValueProperty(new_value)
        else:
            self.data["value"] = new_value
        return self

    def GetUnits(self):
        return self.data["units"]
    
    def SetUnits(self, new_value) -> Measurement:
        if not isinstance(new_value, self.UnitsProperty):
            self.data["units"] = self.UnitsProperty(new_value)
        else:
            self.data["units"] = new_value
        return self

    def Serializable(self) -> dict:
        return self.data
