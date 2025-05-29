import django_filters

from .models import Exercise, Muscle
class ExerciseFilter(django_filters.FilterSet):
    muscles = django_filters.CharFilter(
        method='filter_muscles_intersection'
    )

    def filter_muscles_intersection(self, queryset, name, value):
        if not value:
            return queryset

        for muscle in value.split(','):
            queryset = queryset.filter(muscles__name__icontains=muscle)

        return queryset.distinct()

    class Meta:
        model = Exercise
        fields = ['name', 'muscles']
