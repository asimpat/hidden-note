import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    is_read = django_filters.BooleanFilter(field_name='is_read')

    class Meta:
        model = Message
        fields = {
            'message': ['iexact', 'icontains'],
            'is_read': ['exact']
        }

