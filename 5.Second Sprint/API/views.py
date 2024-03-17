from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response

# Create your views here.
#########################################################################################################################
# End User Authentication:
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class EndUser_Authentication(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Authenticated as an end user."}, status=status.HTTP_200_OK)
        
        else:
            return Response({"message": "You are Not Authenticated as an end user."}, status=status.HTTP_403_FORBIDDEN)
##############################################################################################################

#########################################################################################################################
# Admin User Authentication:
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class AdminUser_Authentication(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Authenticated as an Admin user."}, status=status.HTTP_200_OK)
        
        else:
            return Response({"message": "You are Not Authenticated as an Admin user."}, status=status.HTTP_403_FORBIDDEN)
##############################################################################################################
# Adding Enduser to Admin User Group and removing from Admin Group 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404

@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']

    if username:
        user = get_object_or_404(User, username=username)
        managers_group = Group.objects.get(name="Manager")

        if request.method == 'POST':
            managers_group.user_set.add(user)
            return Response({"message": "User Added"})
        
        elif request.method == 'DELETE':
            managers_group.user_set.remove(user)
            return Response({"message": "User Removed"})
    
    return Response({"message": "error"}) #, status=status.HTTP_400_BAD_REQUEST) 
##############################################################################################################
#Sprint2: Implementing Stream Model

from .models import Stream
from .serializers import StreamSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404

from .Admin_user_Throttle import TwentyCallsPerMinute
from .End_user_Throttle import TenCallsPerMinute

###################################################################
# View for getting Stream Id
@api_view(['POST'])
def get_stream_id(request):

    stream_name = request.data['stream_name']

    if stream_name:
        try:
            stream = Stream.objects.get(stream_name=stream_name)
            stream_id = stream.pk 
            return Response({'stream_id': stream_id}, status=200)
        except Stream.DoesNotExist:
            return Response({'error': 'Stream not found'}, status=404)
    else:
        return Response({'error': 'Stream name not provided'}, status=400)
#####################################################################

# View 1: Create (C)
class StreamCreateView(generics.ListCreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TwentyCallsPerMinute]

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": "You do not have permission to access this resource."},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.validate_stream_name(serializer.initial_data.get('stream_name'))
        serializer.validate_Stream_Existence(serializer.initial_data)
        serializer.save()



# View 2: Read (R)
class StreamRetrieveView(generics.ListAPIView): # get
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TenCallsPerMinute]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# View 3: Update (U)
class StreamUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TwentyCallsPerMinute]

    def put(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"Error": "You do not have permission to access this resource."},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        serializer.validate_stream_name(serializer.initial_data.get('stream_name'))
        serializer.validate_Stream_Existence(serializer.initial_data)
        serializer.save()


# View 4: Delete (D)
@permission_classes([IsAdminUser])
class StreamDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TwentyCallsPerMinute]

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            instance = self.get_object()
            instance.delete()
            return Response({"succes": "succesfully deleted!!"},status=204)  
        
        else: return Response({"Error": "You do not have permission to access this resource."},
                            status=status.HTTP_403_FORBIDDEN)  
############################################################################################################
