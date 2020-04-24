from __future__ import annotations
from collections import UserDict

class ConfigPayload(UserDict):
    """This represents a JSON object.
    """
    class DeviceClassProperty(object):
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

        def Set(self, new_value) -> ConfigPayload.DeviceClassProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a ConfigPayload.DeviceClassProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class NameProperty(object):
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

        def Set(self, new_value) -> ConfigPayload.NameProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a ConfigPayload.NameProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class StateTopicProperty(object):
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

        def Set(self, new_value) -> ConfigPayload.StateTopicProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a ConfigPayload.StateTopicProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class UnitOfMeasurementProperty(object):
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

        def Set(self, new_value) -> ConfigPayload.UnitOfMeasurementProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a ConfigPayload.UnitOfMeasurementProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()

    class ValueTemplateProperty(object):
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

        def Set(self, new_value) -> ConfigPayload.ValueTemplateProperty:
            if isinstance(new_value, type(self)):
                self._value = new_value._value
            elif isinstance(new_value, str):
                self._Validate(new_value)
                self._value = new_value
            else:
                raise TypeError("The provided type was not a ConfigPayload.ValueTemplateProperty or a str")
            return self

        def Get(self) -> str:
            return self._value

        def Serializable(self) -> str:
            return self.Get()


    def __init__(self, data=None, **kwargs):
        """Initialization for the ConfigPayload object.
        It can be initialized with an object, or by passing each
        object property as a keyword argument.
        """
        new_data = {}
        try:
            prop = data["device_class"] if ("device_class" in data) else kwargs["device_class"]
            if not isinstance(prop, self.DeviceClassProperty):
                new_data["device_class"] = self.DeviceClassProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["name"] if ("name" in data) else kwargs["name"]
            if not isinstance(prop, self.NameProperty):
                new_data["name"] = self.NameProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["state_topic"] if ("state_topic" in data) else kwargs["state_topic"]
            if not isinstance(prop, self.StateTopicProperty):
                new_data["state_topic"] = self.StateTopicProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["unit_of_measurement"] if ("unit_of_measurement" in data) else kwargs["unit_of_measurement"]
            if not isinstance(prop, self.UnitOfMeasurementProperty):
                new_data["unit_of_measurement"] = self.UnitOfMeasurementProperty(prop)
        except KeyError:
            pass
        try:
            prop = data["value_template"] if ("value_template" in data) else kwargs["value_template"]
            if not isinstance(prop, self.ValueTemplateProperty):
                new_data["value_template"] = self.ValueTemplateProperty(prop)
        except KeyError:
            pass
        super().__init__(new_data)

    def GetDeviceClass(self):
        return self.data["device_class"]
    
    def SetDeviceClass(self, new_value) -> ConfigPayload:
        if not isinstance(new_value, self.DeviceClassProperty):
            self.data["device_class"] = self.DeviceClassProperty(new_value)
        else:
            self.data["device_class"] = new_value
        return self

    def GetName(self):
        return self.data["name"]
    
    def SetName(self, new_value) -> ConfigPayload:
        if not isinstance(new_value, self.NameProperty):
            self.data["name"] = self.NameProperty(new_value)
        else:
            self.data["name"] = new_value
        return self

    def GetStateTopic(self):
        return self.data["state_topic"]
    
    def SetStateTopic(self, new_value) -> ConfigPayload:
        if not isinstance(new_value, self.StateTopicProperty):
            self.data["state_topic"] = self.StateTopicProperty(new_value)
        else:
            self.data["state_topic"] = new_value
        return self

    def GetUnitOfMeasurement(self):
        return self.data["unit_of_measurement"]
    
    def SetUnitOfMeasurement(self, new_value) -> ConfigPayload:
        if not isinstance(new_value, self.UnitOfMeasurementProperty):
            self.data["unit_of_measurement"] = self.UnitOfMeasurementProperty(new_value)
        else:
            self.data["unit_of_measurement"] = new_value
        return self

    def GetValueTemplate(self):
        return self.data["value_template"]
    
    def SetValueTemplate(self, new_value) -> ConfigPayload:
        if not isinstance(new_value, self.ValueTemplateProperty):
            self.data["value_template"] = self.ValueTemplateProperty(new_value)
        else:
            self.data["value_template"] = new_value
        return self

    def Serializable(self) -> dict:
        return self.data
