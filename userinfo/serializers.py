from rest_framework import serializers
from django.contrib.auth.models import User

from workout.models import Equipment

from .models import UserEquipment, UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    fullname = serializers.SerializerMethodField()

    def validate_age(self, value):
        if value is not None:
            if value > 100:
                raise serializers.ValidationError("Age must be less than or equal to 100.")
            if value < 13:
                raise serializers.ValidationError("Age must be at least 13.")
        return value

    def validate_height(self, value):
        if value is not None and value > 200:
            raise serializers.ValidationError("Height must be less than or equal to 200 cm.")
        return value

    def validate_weight(self, value):
        if value is not None and value > 200:
            raise serializers.ValidationError("Weight must be less than or equal to 200 kg.")
        return value

    def validate_fitness_level(self, value):
        if value and value not in dict(UserInfo.FITNESS_LEVEL_CHOICES):
            raise serializers.ValidationError(f"Invalid fitness level. Choose from: {dict(UserInfo.FITNESS_LEVEL_CHOICES).keys()}")
        return value

    def validate_fitness_goal(self, value):
        if value and value not in dict(UserInfo.FITNESS_GOAL_CHOICES):
            raise serializers.ValidationError(f"Invalid fitness goal. Choose from: {dict(UserInfo.FITNESS_GOAL_CHOICES).keys()}")
        return value

    def get_fullname(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'fullname', 'bio', 'age', 'height', 'weight', 'gender', 'bmi', 'fitness_level', 'fitness_goal', 'frontend_settings']

class UserEquipmentSerializer(serializers.ModelSerializer):
    equipment = serializers.SlugRelatedField(queryset=Equipment.objects.all(), slug_field='name')
    class Meta:
        model = UserEquipment
        fields = ['equipment']
