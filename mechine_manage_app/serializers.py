from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Machine, ToolsInUse, Axis, FieldData
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, including password and confirmation.
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

    def validate(self, data):
        """
        Validate that the password and confirm_password fields match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class MachineSerializer(serializers.ModelSerializer):
    """
    Serializer for Machine model, including custom validations for tool_offset and feedrate.
    """
    class Meta:
        model = Machine
        fields = '__all__'
        extra_kwargs = {
            'machine_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate_tool_offset(self, value):
        """
        Validate that the tool_offset is between 5 and 40.
        """
        if not (5 <= value <= 40):
            raise serializers.ValidationError(
                'Tool offset must be between 5 and 40.')
        return value

    def validate_feedrate(self, value):
        """
        Validate that the feedrate is between 0 and 20000.
        """
        if not (0 <= value <= 20000):
            raise serializers.ValidationError(
                'Feedrate must be between 0 and 20000.')
        return value


class ToolsInUseSerializer(serializers.ModelSerializer):
    """
    Serializer for ToolsInUse model, including validation for tool_in_use based on machine's tool capacity.
    """
    machine_id = serializers.CharField(write_only=True)

    class Meta:
        model = ToolsInUse
        fields = ['machine_id', 'machine',
                  'tool_in_use', 'created_at', 'updated_at']
        extra_kwargs = {
            'machine': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
        depth = 2

    def validate(self, data):
        """
        Ensure that the tool_in_use value is valid based on the machine's tool capacity.
        """
        machine_id = data.get('machine_id')

        if machine_id:
            try:
                machine = Machine.objects.get(machine_id=machine_id)
            except Machine.DoesNotExist:
                raise serializers.ValidationError(
                    {'machine_id': 'Machine with this ID does not exist.'})

            tool_in_use = data.get('tool_in_use')
            if tool_in_use is not None and not (1 <= tool_in_use <= machine.tool_capacity):
                raise serializers.ValidationError(
                    {'tool_in_use': f'Tool in use must be between 1 and {machine.tool_capacity}.'})

        return data

    def create(self, validated_data):
        """
        Create a new ToolsInUse instance with the provided validated data.
        """
        machine_id = validated_data.pop('machine_id')

        try:
            machine = Machine.objects.get(machine_id=machine_id)
        except Machine.DoesNotExist:
            raise serializers.ValidationError(
                {'machine_id': 'Machine with this ID does not exist.'})

        if ToolsInUse.objects.filter(machine=machine).exists():
            raise serializers.ValidationError(
                {'machine_id': 'ToolsInUse for this machine already exists.'})

        return ToolsInUse.objects.create(machine=machine, **validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing ToolsInUse instance with the provided validated data.
        """
        machine_id = validated_data.get('machine_id')

        if machine_id:
            try:
                machine = Machine.objects.get(machine_id=machine_id)
            except Machine.DoesNotExist:
                raise serializers.ValidationError(
                    {'machine_id': 'Machine with this ID does not exist.'})
            instance.machine = machine

        instance.tool_in_use = validated_data.get(
            'tool_in_use', instance.tool_in_use)
        instance.save()
        return instance


class WebsocketDataSerailizer(serializers.ModelSerializer):
    """
    Serializer for Axis model to handle websocket data.
    """
    class Meta:
        model = Axis
        fields = '__all__'
        depth = 3


class FieldDataAxisSerializer(serializers.ModelSerializer):
    """
    Serializer for Axis model to be used within FieldDataSerializer.
    """
    class Meta:
        model = Axis
        fields = ['machine', 'axis_name', 'homed']
        depth = 2


class FieldDataLatestSerializer(serializers.ModelSerializer):
    """
    Serializer for the latest field data, including axis details.
    """
    axis = FieldDataAxisSerializer()

    class Meta:
        model = FieldData
        fields = ['axis', 'created_at', 'actual_position',
                  'target_position', 'distance_to_go', 'acceleration', 'velocity']


class AxisSerializer(serializers.ModelSerializer):
    """
    Serializer for Axis model, including custom validation using the clean method.
    """
    class Meta:
        model = Axis
        fields = '__all__'
        extra_kwargs = {
            'machine': {'required': False}
        }

    def validate(self, data):
        """
        Ensure that the custom validation in the Axis model's clean() method is called.
        """
        instance = Axis(**data)

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data


