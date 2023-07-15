from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        # To show all Fields in the Model, or Use
        # fields = ['id', 'name', ...]
        fields = '__all__'
