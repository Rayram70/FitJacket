# workoutplans/urls.py
from django.urls import path
from . import views

app_name = 'workoutplans'

urlpatterns = [
    path('', views.workout_plan_request, name='request'),
    path('results/', views.workout_plan_results, name='results'),
    path('save/', views.save_plan, name='save_plan'),
    path('saved/', views.saved_plans, name='saved_list'),  # ⭐️ THIS was missing!
    path('view/<int:plan_id>/', views.view_plan, name='view_plan'),  # ⭐️ Also for the "🔍 View"
    path('delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
]