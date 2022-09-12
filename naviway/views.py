from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Count, Max, Min, ExpressionWrapper
from django.db.models.functions import TruncDay, TruncHour
import requests
import psycopg2

def home(request):
    return render(request, 'home.html')

