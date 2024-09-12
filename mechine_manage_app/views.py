from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from .models import Machine, ToolsInUse, FieldData, Axis
from .serializers import MachineSerializer, UserRegisterSerializer,MachineSerializerForSingle, FieldDataLatestSerializer, ToolsInUseSerializer, AxisSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import CustomPermissionsExceptToolsInUse,CustomPermissionsForToolsInUse,ReadingDataPermission
from django.utils.timezone import now
from datetime import timedelta


class RegisterView(APIView):
    """
    API view to handle user registration and return JWT tokens.
    """
    def post(self, request):
        """
        Register a new user and return JWT tokens.
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MachineViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing Machine instances.
    """
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [CustomPermissionsExceptToolsInUse]

    def get_object(self):
        """
        Retrieve a Machine instance by machine_id.
        """
        machine_id = self.kwargs.get("machine_id")
        try:
            return Machine.objects.get(machine_id=machine_id)
        except Machine.DoesNotExist:
            raise NotFound(f"Machine with machine_id {machine_id} not found.")

class MachineViewSetForSingleData(viewsets.ModelViewSet):
    """
    API viewset for managing Machine instances.
    """
    queryset = Machine.objects.all()
    serializer_class = MachineSerializerForSingle
    permission_classes = [CustomPermissionsExceptToolsInUse]

    def get_object(self):
        """
        Retrieve a Machine instance by machine_id.
        """
        machine_id = self.kwargs.get("machine_id")
        try:
            return Machine.objects.get(machine_id=machine_id)
        except Machine.DoesNotExist:
            raise NotFound(f"Machine with machine_id {machine_id} not found.")

    

class ToolsInUseViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing ToolsInUse instances.
    """
    queryset = ToolsInUse.objects.all()
    serializer_class = ToolsInUseSerializer
    permission_classes = [CustomPermissionsForToolsInUse]

    def get_object(self):
        """
        Retrieve ToolsInUse instance by machine_id.
        """
        machine_id = self.kwargs.get("machine_id")
        try:
            return ToolsInUse.objects.get(machine__machine_id=machine_id)
        except ToolsInUse.DoesNotExist:
            raise NotFound(
                f"ToolsInUse for machine_id {machine_id} not found.")


class AxisViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing Axis instances.
    """
    serializer_class = AxisSerializer
    permission_classes = [CustomPermissionsExceptToolsInUse]

    def get_queryset(self):
        """
        Retrieve Axis instances filtered by machine_id.
        """
        machine_id = self.kwargs.get("machine_id")
        return Axis.objects.filter(machine__machine_id=machine_id)

    def get_object(self):
        """
        Retrieve an Axis instance by machine_id and axis_name.
        """
        machine_id = self.kwargs.get("machine_id")
        axis_name = self.kwargs.get("axis_name")
        try:
            return Axis.objects.get(machine__machine_id=machine_id, axis_name=axis_name)
        except Axis.DoesNotExist:
            raise NotFound(f"Axis {axis_name} for Machine {machine_id} not found.")
        
    def perform_create(self, serializer):
        """
        Handle creation of a new Axis instance with validation.
        """
        machine_id = self.kwargs.get("machine_id")
        try:
            machine = Machine.objects.get(machine_id=machine_id)
        except Machine.DoesNotExist:
            raise NotFound(f"Machine with machine_id {machine_id} not found.")
        
        axis_name = serializer.validated_data['axis_name']
        if Axis.objects.filter(machine=machine, axis_name=axis_name).exists():
            raise ValidationError(f"Axis {axis_name} already exists for Machine {machine_id}.")
        serializer.save(machine=machine)

    def perform_update(self, serializer):
        """
        Handle update of an existing Axis instance with validation.
        """
        machine_id = self.kwargs.get("machine_id")
        try:
            machine = Machine.objects.get(machine_id=machine_id)
        except Machine.DoesNotExist:
            raise NotFound(f"Machine with machine_id {machine_id} not found.")
        
        instance = self.get_object()

        new_axis_name = serializer.validated_data.get('axis_name', instance.axis_name)

        if Axis.objects.filter(machine=machine, axis_name=new_axis_name).exclude(id=instance.id).exists():
            raise ValidationError(f"Axis {new_axis_name} already exists for Machine {machine_id}.")
        
        serializer.save(machine=machine)


class MachineHistoricalDataView(APIView):
    """
    API view to retrieve historical data for a specified machine and axes.
    """
    # permission_classes = [ReadingDataPermission]

    def get(self, request, *args, **kwargs):
        """
        Retrieve historical field data for a machine and specified axes.
        """
        axis_names = request.query_params.getlist('axis_names')
        machine_id = request.query_params.get('machine_id')

        if not axis_names or not machine_id:
            return Response({"error": "Both axis_names and machine_id must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            machine = Machine.objects.get(machine_id=machine_id)

            if not Axis.objects.filter(machine=machine).exists():
                return Response({"error": "No axes found for the specified machine."}, status=status.HTTP_404_NOT_FOUND)

            try:
                tools_in_use = ToolsInUse.objects.get(machine=machine)
                tool_in_use_data = tools_in_use.tool_in_use

            except ToolsInUse.DoesNotExist:
                tool_in_use_data = None

            time_threshold = now() - timedelta(minutes=15)

            axis_objects = Axis.objects.filter(
                machine=machine,
                axis_name__in=axis_names
            )

            axis_ids = axis_objects.values_list('id', flat=True)
            field_data_query = FieldData.objects.filter(
                axis__id__in=axis_ids,
                created_at__gte=time_threshold
            )

            serializer = FieldDataLatestSerializer(field_data_query, many=True)

            response_data = {
                "machine_tools_in_use": tool_in_use_data,
                "field_data": serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Machine.DoesNotExist:
            return Response({"error": "The specified machine ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


