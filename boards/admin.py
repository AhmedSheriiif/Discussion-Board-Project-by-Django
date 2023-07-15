from django.contrib import admin
from .models import Board

# To make admin can add Board
admin.site.register(Board)
