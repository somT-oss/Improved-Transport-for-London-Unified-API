from django.urls import path 
from . import views 

urlpatterns = [
    path('accident-stats/<int:year>', views.get_accidents_stats, name='accident-stats'),
    path('accident-stats/<int:year>/range/<int:start_date>/<int:end_date>', views.get_accidents_stats_with_range, name='accident-stats-with-range'),
]