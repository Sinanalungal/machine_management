from django.core.exceptions import ValidationError
from django.db import models

class Machine(models.Model):
    """
    Model representing a machine with its properties and validation.
    """
    machine_id = models.CharField(max_length=50, unique=True)
    machine_name = models.CharField(max_length=100, unique=True)
    tool_capacity = models.IntegerField()
    tool_offset = models.FloatField()
    feedrate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['machine_id']),
            models.Index(fields=['machine_name']),
        ]
        
    

    def __str__(self):
        return self.machine_name

    def clean(self):
        """
        Validate the Machine instance's attributes.
        
        Raises:
            ValidationError: If tool_offset or feedrate are outside of the allowed ranges.
        """
        if not (5 <= self.tool_offset <= 40):
            raise ValidationError('Tool offset must be between 5 and 40.')

        if not (0 <= self.feedrate <= 20000):
            raise ValidationError('Feedrate must be between 0 and 20000.')

class ToolsInUse(models.Model):
    """
    Model representing tools in use for a specific machine.
    """
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE)
    tool_in_use = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['machine']),
        ]
       

        

    def __str__(self):
        return str(self.tool_in_use)

    def clean(self):
        """
        Validate the ToolsInUse instance's attributes.
        
        Raises:
            ValidationError: If tool_in_use is outside of the allowed range.
        """
        if self.tool_in_use is not None:
            if not (1 <= self.tool_in_use <= self.machine.tool_capacity):
                raise ValidationError(f'Tool in use must be between 1 and {self.machine.tool_capacity}.')

class Axis(models.Model):
    """
    Model representing an axis of a machine with its properties and validation.
    """
    AXIS_CHOICES = [
        ('X', 'X'),
        ('Y', 'Y'),
        ('Z', 'Z'),
        ('A', 'A'),
        ('C', 'C')
    ]
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    axis_name = models.CharField(max_length=1, choices=AXIS_CHOICES)
    max_acceleration = models.FloatField()
    max_velocity = models.FloatField()
    actual_position = models.FloatField()
    target_position = models.FloatField()
    homed = models.BooleanField()
    acceleration = models.FloatField()
    velocity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['machine']),
            models.Index(fields=['axis_name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['axis_name', 'machine'], name='unique_axis_for_machine')
        ]
        

    def __str__(self):
        return f"{self.axis_name} of {self.machine.machine_name}"

    def clean(self):
        """
        Validate the Axis instance's attributes.
        
        Raises:
            ValidationError: If any attribute is outside of the allowed range.
        """
        if not (-190 <= self.actual_position <= 190):
            raise ValidationError('Actual position must be between -190 and 190.')

        if not (-190 <= self.target_position <= 191):
            raise ValidationError('Target position must be between -190 and 191.')

        if not (0 <= self.acceleration <= 150):
            raise ValidationError('Acceleration must be between 0 and 150.')

        if not (0 <= self.velocity <= 80):
            raise ValidationError('Velocity must be between 0 and 80.')

class FieldData(models.Model):
    """
    Model representing field data for an axis, including position, distance, acceleration, and velocity.
    """
    axis = models.ForeignKey(Axis, on_delete=models.CASCADE)
    actual_position = models.FloatField()
    target_position = models.FloatField()
    distance_to_go = models.FloatField()
    acceleration = models.FloatField()
    velocity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['axis']),
        ]

    def clean(self):
        """
        Validate the FieldData instance's attributes.
        
        Raises:
            ValidationError: If any attribute is invalid.
        """
        if self.distance_to_go != (self.target_position - self.actual_position):
            raise ValidationError('Distance to go must be target_position - actual_position.')

        if not (0 <= self.acceleration <= 150):
            raise ValidationError('Acceleration must be between 0 and 150.')

        if not (0 <= self.velocity <= 80):
            raise ValidationError('Velocity must be between 0 and 80.')
