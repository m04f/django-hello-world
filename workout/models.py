from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.query import Q, F
import uuid

from rest_framework.generics import ValidationError

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    muscles = models.ManyToManyField('Muscle', through='ExerciseMuscle')
    equipments = models.ManyToManyField('Equipment')

    def __str__(self):
        return self.name


class ExerciseMuscle(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    muscle = models.ForeignKey('Muscle', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exercise} - {self.muscle}"


class Muscle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    exercises = models.ManyToManyField('Exercise', through='ExerciseMuscle')

    def __str__(self):
        return self.name

class Workout(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    estimated_time = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exercises = models.ManyToManyField('Exercise', through='WorkoutExercise')
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=False)

    class Meta:
        unique_together = ('creator', 'name')

class WorkoutExercise(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    duration = models.PositiveSmallIntegerField(null=True)
    reps = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    sets = models.PositiveSmallIntegerField(default=1)
    rest = models.PositiveSmallIntegerField(default=120)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('workout', 'order')
        ordering = ['order']
        constraints = [
            models.CheckConstraint(
                check=Q(duration__isnull=False) | Q(reps__isnull=False),
                name='workout_either_duration_or_reps_notnull',
                violation_error_message='Either duration or reps must be provided'
            )
        ]

class PlanWorkout(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, db_index=True)
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT, db_index=True)
    day = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True)

class Plan(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, db_index=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    workouts = models.ManyToManyField(Workout, through=PlanWorkout)
    public = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = ('creator', 'name')

class Equipment(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
