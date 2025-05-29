from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models import Q
import uuid

from rest_framework.generics import ValidationError

from workout.models import Exercise, Plan, PlanWorkout, Workout

class UserPlanWorkout(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT)
    record = models.ForeignKey('WorkoutRecord', on_delete=models.SET_NULL, null=True)
    userplan = models.ForeignKey('UserPlan', on_delete=models.CASCADE, editable=False, db_index=True)
    date = models.DateField()

class UserPlan(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    start_date = models.DateField(auto_now=True, editable=False)
    workouts = models.ManyToManyField('WorkoutRecord', through=UserPlanWorkout)

    class Meta:
        unique_together = ('plan', 'user')


class WorkoutRecord(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT, db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    duration = models.PositiveIntegerField(null=True)


class ExerciseRecord(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    workout_record = models.ForeignKey(WorkoutRecord, null=True, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(null=True)
    reps = models.PositiveSmallIntegerField(null=True)
    duration = models.PositiveIntegerField(null=True)
    rest = models.PositiveIntegerField(null=True)
    notes = models.TextField(blank=True)
    pre = models.PositiveSmallIntegerField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(pre__lte=10),
                name='pre_lte_10'
            ),
            models.CheckConstraint(
                check=Q(duration__isnull=False) | Q(reps__isnull=False),
                name='either_duration_or_reps_notnull',
                violation_error_message='Either duration or reps must be provided'
            )
        ]
