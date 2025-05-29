from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response

from workout.views import EquipmentsView

from .serializers import UserEquipmentSerializer, UserInfoSerializer
from .models import UserEquipment, UserInfo

class UserInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        userinfo, _ = UserInfo.objects.get_or_create(user=self.request.user)
        return userinfo

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user)

class UserEquipmentsView(generics.ListCreateAPIView):
    serializer_class = UserEquipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserEquipment.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        equipment_names = queryset.values_list('equipment__name', flat=True)
        return Response(list(equipment_names))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
