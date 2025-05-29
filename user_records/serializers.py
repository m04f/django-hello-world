from datetime import timedelta
from rest_framework import serializers
from django.db import transaction
from django.db.utils import DatabaseError, IntegrityError

from workout.models import Exercise, Plan, PlanWorkout

from .models import ExerciseRecord, UserPlan, UserPlanWorkout, WorkoutRecord


class ExerciseRecordSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercise.objects.all(), slug_field='name')
    workout_record = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ExerciseRecord
        fields = ['uuid', 'workout_record', 'exercise', 'reps', 'weight', 'pre', 'datetime', 'rest', 'duration']

    def validate(self, attrs):
        """
        Check that either duration or reps is provided.
        """
        if attrs.get('duration') is None and attrs.get('reps') is None:
            raise serializers.ValidationError("Either duration or reps must be provided")
        return attrs


class WorkoutRecordSerializer(serializers.ModelSerializer):
    exercises = ExerciseRecordSerializer(many=True, read_only=False, required=False, source='exerciserecord_set')
    workout_name = serializers.CharField(source='workout.name', read_only=True)

    class Meta:
        model = WorkoutRecord
        fields = ['uuid', 'duration', 'workout', 'workout_name', 'exercises', 'datetime']


class UserPlanWorkoutSerializer(serializers.ModelSerializer):
    workout = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='workout.name')

    class Meta:
        model = UserPlanWorkout
        fields = ['uuid', 'name', 'workout', 'record', 'date']


class UserPlanSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())
    workouts = UserPlanWorkoutSerializer(many=True, source='userplanworkout_set', read_only=True)


    def create(self, validated_data):
        try:
            with transaction.atomic():
                userplan = UserPlan.objects.create(**validated_data)
                plan_workouts = PlanWorkout.objects.filter(plan=userplan.plan)
                workouts = [
                    UserPlanWorkout(userplan=userplan, date=userplan.start_date+timedelta(days=plan_workout.day-1), record=None, workout=plan_workout.workout)
                    for plan_workout in plan_workouts
                ]
                UserPlanWorkout.objects.bulk_create(workouts)
                return userplan
        except IntegrityError as e:
            raise serializers.ValidationError(f"Integrity error: {str(e)}")
        except DatabaseError as e:
            raise serializers.ValidationError(f"Database error: {str(e)}")

    class Meta:
        model = UserPlan
        fields = ['uuid', 'plan', 'start_date', 'workouts']
