from django.urls import path

from .views import (
    ExerciseRecordView,
    SingleExerciseRecordView,
    WorkoutRecordsView,
    SingleWorkoutRecordView,
    UserPlansView,
    SingleUserPlansView,
    PlanWorkoutsView,
    SinglePlanWorkoutsView,
)

urlpatterns = [
    path('exercises/', ExerciseRecordView.as_view(), name='exercise-records'),
    path('exercises/<uuid:pk>/', SingleExerciseRecordView.as_view(), name='exercise-record-details'),
    path('workouts/', WorkoutRecordsView.as_view(), name='workout-records'),
    path('workouts/<uuid:pk>/', SingleWorkoutRecordView.as_view(), name='workout-record-details'),
    path('workouts/<uuid:workout_uuid>/exercises', ExerciseRecordView.as_view(), name='workout-exercise-records'),
    path('plans/', UserPlansView.as_view(), name='user-plans'),
    path('plans/<uuid:pk>/', SingleUserPlansView.as_view(), name='user-plan-details'),
    path('plans/<uuid:userplan_uuid>/workouts', PlanWorkoutsView.as_view(), name='user-plan-workouts'),
    path('plans/<uuid:userplan_uuid>/workouts/<uuid:pk>', SinglePlanWorkoutsView.as_view(), name='user-plan-workouts'),
]
