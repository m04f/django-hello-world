from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


from .models import Equipment, Exercise, Muscle, Workout, WorkoutExercise, Plan
from .serializers import ExerciseSerializer, MuscleSerializer, WorkoutSerializer, ExerciseWorkoutSerializer, PlanSerializer, EquipmentSerializer
from .filters import ExerciseFilter
from .permissions import IsAuthorOrReadOnly, IsObjectVisible


class ExerciseView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'muscles__name']
    ordering_fields = ['name']
    filterset_class = ExerciseFilter



class MuscleView(generics.ListAPIView):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name']


class WorkoutsView(generics.ListCreateAPIView):

    def get_queryset(self):
        workouts = Workout.objects.filter(public=True).prefetch_related('workoutexercise_set', 'workoutexercise_set__exercise')
        if self.request.user.is_authenticated:
            workouts = workouts.union(Workout.objects.filter(creator=self.request.user).prefetch_related('workoutexercise_set', 'workoutexercise_set__exercise'))
        return workouts

    serializer_class = WorkoutSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SingleWorkoutView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()

    serializer_class = WorkoutSerializer


    permission_classes = [IsObjectVisible, IsAuthorOrReadOnly]

class PlanView(generics.ListCreateAPIView):
    def get_queryset(self):
        plans = Plan.objects.filter(public=True).prefetch_related('planworkout_set__workout')
        if self.request.user.is_authenticated:
            plans = plans.union(Plan.objects.filter(creator=self.request.user).prefetch_related('planworkout_set__workout'))
        return plans

    serializer_class = PlanSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SinglePlanView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()

    serializer_class = PlanSerializer
    permission_classes = [IsObjectVisible, IsAuthorOrReadOnly]

class SingleExerciseView(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'name'

class SingleMuscleView(generics.RetrieveAPIView):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    lookup_field = 'name'

class EquipmentsView(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
