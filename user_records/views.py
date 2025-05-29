from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserPlanWorkout, WorkoutRecord, ExerciseRecord, UserPlan
from .serializers import UserPlanWorkoutSerializer, WorkoutRecordSerializer, ExerciseRecordSerializer, UserPlanSerializer


class WorkoutRecordsView(generics.ListCreateAPIView):
    def get_queryset(self):
        return WorkoutRecord.objects.filter(user=self.request.user).prefetch_related('exerciserecord_set__exercise')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    serializer_class = WorkoutRecordSerializer
    permission_classes = [IsAuthenticated]


class SingleWorkoutRecordView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return WorkoutRecord.objects.filter(user=self.request.user).prefetch_related('exerciserecord_set__exercise')

    serializer_class = WorkoutRecordSerializer
    permission_classes = [IsAuthenticated]


class ExerciseRecordView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = ExerciseRecord.objects.filter(user=self.request.user)
        workout_pk = self.kwargs.get('workout_uuid')
        if workout_pk:
            queryset = queryset.filter(workout_record__pk=workout_pk)
        return queryset

    def perform_create(self, serializer):
        workout_pk = self.kwargs.get('workout_uuid')
        if workout_pk:
            workout_record = WorkoutRecord.objects.get(pk=workout_pk)
            serializer.save(user=self.request.user, workout_record=workout_record)
        else:
            serializer.save(user=self.request.user)

    serializer_class = ExerciseRecordSerializer
    permission_classes = [IsAuthenticated]


class SingleExerciseRecordView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return ExerciseRecord.objects.filter(user=self.request.user)

    serializer_class = ExerciseRecordSerializer
    permission_classes = [IsAuthenticated]


class UserPlansView(generics.ListCreateAPIView):
    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]


class SingleUserPlansView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user)

    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]

class PlanWorkoutsView(generics.ListAPIView):
    def get_queryset(self):
        userplan_uuid = self.kwargs.get('userplan_uuid')
        return UserPlanWorkout.objects.filter(userplan_id=userplan_uuid, userplan__user=self.request.user)

    serializer_class = UserPlanWorkoutSerializer
    permission_classes = [IsAuthenticated]

class SinglePlanWorkoutsView(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        userplan_uuid = self.kwargs.get('userplan_uuid')
        return UserPlanWorkout.objects.filter(userplan_id=userplan_uuid, userplan__user=self.request.user)

    serializer_class = UserPlanWorkoutSerializer
    permission_classes = [IsAuthenticated]
