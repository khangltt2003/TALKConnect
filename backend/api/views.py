from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import UserProfile, Event
from .serializers import UserSerializer, UserProfileSerializer, EventSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register(request):
  if request.method == 'POST':
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', "POST", 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
  try:
    user = request.user  
  except UserProfile.DoesNotExist:
    return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    profile = UserProfile.objects.get(user = user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)

  elif request.method == "POST":
    requested_data = request.data.copy()
    requested_data['user'] = user.id
    serializer = UserProfileSerializer(data = requested_data, context={'request': request})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status =status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  elif request.method == 'PATCH':
    serializer = UserProfileSerializer(user.profile, data=request.data, partial=True)
    if serializer.is_valid(): 
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def event_list_create(request):
  if request.method == 'GET':
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def event_detail(request, pk):
  event = get_object_or_404(Event, pk=pk)

  if request.method == 'GET':
    serializer = EventSerializer(event)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'PATCH':
    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def participate_event(request, event_id):
  event = get_object_or_404(Event, id=event_id)
  profile = request.user.userprofile

  if request.method == 'POST':
    if profile not in event.participants.all() and event.available_slots > 0:
      event.participants.add(profile)
      event.available_slots -= 1
      event.save()
      return Response({'status': 'participated'}, status=status.HTTP_200_OK)
    return Response({'error': 'Unable to participate'}, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    if profile in event.participants.all():
      event.participants.remove(profile)
      event.available_slots += 1
      event.save()
      return Response({'status': 'left'}, status=status.HTTP_200_OK)
    return Response({'error': 'Unable to leave'}, status=status.HTTP_400_BAD_REQUEST)
