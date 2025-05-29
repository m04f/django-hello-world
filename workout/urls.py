from django.urls import path

from .views import ExerciseView, MuscleView, SingleWorkoutView, WorkoutsView, PlanView, SinglePlanView, SingleExerciseView, SingleMuscleView, EquipmentsView

urlpatterns = [
    path('exercises/', ExerciseView.as_view(), name='exercises'),
    path('exercises/<str:name>', SingleExerciseView.as_view(), name='exercise-details'),
    path('muscles/', MuscleView.as_view(), name='muscles'),
    path('muscles/<str:name>', SingleMuscleView.as_view(), name='muscle-details'),
    path('workouts/', WorkoutsView.as_view(), name='workouts'),
    path('workouts/<uuid:pk>/', SingleWorkoutView.as_view(), name='workout-details'),
    path('plans/', PlanView.as_view(), name='plans'),
    path('plans/<uuid:pk>/', SinglePlanView.as_view(), name='plan-details'),
    path('equipments/', EquipmentsView.as_view(), name='equipment'),
]
