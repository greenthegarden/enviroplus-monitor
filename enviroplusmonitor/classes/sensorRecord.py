from __future__ import annotations
from collections import UserDict
from collections import UserList

class SensorRecord(UserDict):
    """This represents a JSON object.
    """
    class SensorProperty(object):
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

        def Set(self, new_value) -> SensorRecord.SensorProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a SensorRecord.SensorProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class MeasurementsProperty (UserList):
        """ This represents a JSON array.
        """
        class Item(UserDict):
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

                def Set(self, new_value) -> SensorRecord.MeasurementsProperty.Item.LabelProperty:
                    if isinstance(new_value, type(self)):
                        self._value = new_value._value
                    elif isinstance(new_value, str):
                        self._Validate(new_value)
                        self._value = new_value
                    else:
                        raise TypeError("The provided type was not a SensorRecord.MeasurementsProperty.Item.LabelProperty or a str")
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

                def Set(self, new_value) -> SensorRecord.MeasurementsProperty.Item.ValueProperty:
                    if isinstance(new_value, type(self)):
                        self._value = new_value._value
                    elif isinstance(new_value, float):
                        self._Validate(new_value)
                        self._value = new_value
                    elif isinstance(new_value, int):
                        self._Validate(float(new_value))
                        self._value = float(new_value)
                    else:
                        raise TypeError("The provided type was not a SensorRecord.MeasurementsProperty.Item.ValueProperty or a float")
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

                def Set(self, new_value) -> SensorRecord.MeasurementsProperty.Item.UnitsProperty:
                    if isinstance(new_value, type(self)):
                        self._value = new_value._value
                    elif isinstance(new_value, str):
                        self._Validate(new_value)
                        self._value = new_value
                    else:
                        raise TypeError("The provided type was not a SensorRecord.MeasurementsProperty.Item.UnitsProperty or a str")
                    return self

                def Get(self) -> str:
                    return self._value

                def Serializable(self) -> str:
                    return self.Get()


            def __init__(self, data=None, **kwargs):
                """Initialization for the Item object.
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
            
            def SetLabel(self, new_value) -> SensorRecord.MeasurementsProperty.Item:
                if not isinstance(new_value, self.LabelProperty):
                    self.data["label"] = self.LabelProperty(new_value)
                else:
                    self.data["label"] = new_value
                return self

            def GetValue(self):
                return self.data["value"]
            
            def SetValue(self, new_value) -> SensorRecord.MeasurementsProperty.Item:
                if not isinstance(new_value, self.ValueProperty):
                    self.data["value"] = self.ValueProperty(new_value)
                else:
                    self.data["value"] = new_value
                return self

            def GetUnits(self):
                return self.data["units"]
            
            def SetUnits(self, new_value) -> SensorRecord.MeasurementsProperty.Item:
                if not isinstance(new_value, self.UnitsProperty):
                    self.data["units"] = self.UnitsProperty(new_value)
                else:
                    self.data["units"] = new_value
                return self

            def Serializable(self) -> dict:
                return self.data

        
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
        """Initialization for the SensorRecord object.
        It can be initialized with an object, or by passing each
        object property as a keyword argument.
        """
        new_data = {}
        try:
            prop = data["sensor"] if ("sensor" in data) else kwargs["sensor"]
            if not isinstance(prop, self.SensorProperty):
                new_data["sensor"] = self.SensorProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'sensor'")
        try:
            prop = data["measurements"] if ("measurements" in data) else kwargs["measurements"]
            if not isinstance(prop, self.MeasurementsProperty):
                new_data["measurements"] = self.MeasurementsProperty(prop)
        except KeyError:
            raise ValueError("Missing property 'measurements'")
        super().__init__(new_data)

    def GetSensor(self):
        return self.data["sensor"]
    
    def SetSensor(self, new_value) -> SensorRecord:
        if not isinstance(new_value, self.SensorProperty):
            self.data["sensor"] = self.SensorProperty(new_value)
        else:
            self.data["sensor"] = new_value
        return self

    def GetMeasurements(self):
        return self.data["measurements"]
    
    def SetMeasurements(self, new_value) -> SensorRecord:
        if not isinstance(new_value, self.MeasurementsProperty):
            self.data["measurements"] = self.MeasurementsProperty(new_value)
        else:
            self.data["measurements"] = new_value
        return self

    def Serializable(self) -> dict:
        return self.data
