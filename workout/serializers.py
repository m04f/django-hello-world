from rest_framework import serializers
from django.db import transaction
from django.db.utils import DatabaseError, IntegrityError

from .models import Equipment, Exercise, Muscle, Plan, PlanWorkout, Workout, WorkoutExercise


class MuscleSerializer(serializers.ModelSerializer):
    exercises = serializers.HyperlinkedRelatedField(view_name='exercise-details', many=True, queryset=Exercise.objects.all(), lookup_field='name')
    class Meta:
        model = Muscle
        fields = ['name', 'description', 'exercises']

class ExerciseSerializer(serializers.ModelSerializer):
    muscles = serializers.HyperlinkedRelatedField(view_name='muscle-details', many=True, queryset=Muscle.objects.all(), lookup_field='name')
    equipments = serializers.SlugRelatedField(many=True, queryset=Equipment.objects.all(), slug_field='name')

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'muscles', 'equipments']


class ExerciseWorkoutSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercise.objects.all(), slug_field='name')

    class Meta:
        model = WorkoutExercise
        fields = ['uuid', 'exercise', 'reps', 'sets', 'weight', 'rest', 'duration']

    def validate(self, attrs):
        """
        Check that either duration or reps is provided.
        """
        if attrs.get('duration') is None and attrs.get('reps') is None:
            raise serializers.ValidationError("Either duration or reps must be provided")
        return attrs


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    exercises = ExerciseWorkoutSerializer(many=True, source='workoutexercise_set', required=False)
    exercise_names = serializers.SlugRelatedField(many=True, queryset=Exercise.objects.all(), slug_field='name', source='exercises', required=False)
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    total_duration = serializers.SerializerMethodField()

    def to_representation(self, instance):
        """
        Dynamically include exercises field only for workout-details endpoint.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.resolver_match and request.resolver_match.url_name != 'workout-details':
            representation.pop('exercises', None)
        else:
            representation.pop('exercise_names', None)
        return representation

    def get_total_duration(self, obj):
        """
        Calculate the total duration of the workout based on its exercises.
        """
        total_seconds = sum(
            ((exercise.duration or (exercise.reps or 0) * 3) * exercise.sets) + (exercise.rest * exercise.sets)
            for exercise in obj.workoutexercise_set.all()
        )
        return total_seconds

    def get_exercise_names(self, obj):
        """
        Get the names of exercises in the workout.
        """
        return [exercise.name for exercise in obj.workoutexercise_set.all()]

    def create(self, validated_data):

        exercises_data = validated_data.pop('workoutexercise_set')
        try:
            with transaction.atomic():
                workout = Workout.objects.create(**validated_data)
                workoutexercises = [
                    WorkoutExercise(workout=workout, order=i+1, **exercise_data)
                    for i, exercise_data in enumerate(exercises_data)
                ]
                WorkoutExercise.objects.bulk_create(workoutexercises)
                return workout
        except IntegrityError as e:
            raise serializers.ValidationError(f"integrity error: {str(e)}")
        except DatabaseError as e:
            raise serializers.ValidationError(f"Database error: {str(e)}")

    def update(self, instance, validated_data):
        """
        Update an existing workout and its related exercises.
        """
        exercises_data = validated_data.pop('workoutexercise_set', None)
        try:
            with transaction.atomic():
                # Update the workout instance
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()

                if exercises_data is not None:
                    # Clear existing exercises
                    instance.workoutexercise_set.all().delete()

                    # Add updated exercises
                    workoutexercises = [
                        WorkoutExercise(workout=instance, order=i+1, **exercise_data)
                        for i, exercise_data in enumerate(exercises_data)
                    ]
                    WorkoutExercise.objects.bulk_create(workoutexercises)

                return instance
        except IntegrityError as e:
            raise serializers.ValidationError(f"integrity error: {str(e)}")
        except DatabaseError as e:
            raise serializers.ValidationError(f"Database error: {str(e)}")

    class Meta:
        model = Workout
        fields = ['url', 'uuid', 'name', 'creator', 'description', 'exercises', 'exercise_names', 'notes', 'public', 'total_duration']
        extra_kwargs = {
            'url': {'view_name': 'workout-details'}
        }


class PlanWorkoutSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='workout.name', read_only=True)
    workout = serializers.HyperlinkedRelatedField(view_name='workout-details', queryset=Workout.objects.all())
    workout_uuid = serializers.UUIDField(source='workout.uuid')

    class Meta:
        model = PlanWorkout
        fields = ['uuid', 'name', 'workout_uuid', 'workout', 'day', 'notes']


class PlanSerializer(serializers.ModelSerializer):
    workouts = PlanWorkoutSerializer(many=True, source='planworkout_set')

    class Meta:
        model = Plan
        fields = ['uuid', 'creator', 'name', 'description', 'workouts',  'public']


class EquipmentSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(many=True, source='exerciseequipment_set', read_only=True)

    class Meta:
        model = Equipment
        fields = ['uuid', 'name', 'exercises']
