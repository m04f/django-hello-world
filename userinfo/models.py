from django.db import models
from django.contrib.auth.models import User

from workout.models import Equipment, Plan

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default='Welcome! Remember, every journey begins with a single step.')
    age = models.PositiveSmallIntegerField(null=True, blank=True, default=25)
    height = models.PositiveSmallIntegerField(null=True, blank=True, default=175)
    weight = models.PositiveSmallIntegerField(null=True, blank=True, default=70)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True, db_index=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    FITNESS_LEVEL_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    fitness_level = models.CharField(max_length=20 , choices=FITNESS_LEVEL_CHOICES, null=True, blank=True, db_index=True, default='beginner')
    FITNESS_GOAL_CHOICES = [('lose weight', 'Lose Weight'), ('gain weight', 'Gain Weight'), ('maintain weight', 'Maintain Weight')]
    fitness_goal = models.CharField(max_length=20, choices=FITNESS_GOAL_CHOICES, null=True, blank=True, db_index=True, default='lose weight')
    frontend_settings = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__lte=100), name='age_lte_100'),
            models.CheckConstraint(check=models.Q(age__gte=13), name='age_gte_13'),
            models.CheckConstraint(check=models.Q(height__lte=200), name='height_lte_200'),
            models.CheckConstraint(check=models.Q(weight__lte=200), name='weight_lte_200'),
        ]

class UserEquipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'equipment')
