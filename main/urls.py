from django.urls import path
from . import views
from .views import eligibility_check, violation_comparator, eligibility_check_page


urlpatterns = [
    path("", views.home, name="home"),
    path("eligibility_check_page/", views.eligibility_check_page, name="eligibility_check_page"),
    path("violation_comparator_page/", views.violation_comparator_page, name="violation_comparator_page"),
    path('eligibility_check/', eligibility_check, name='eligibility_check'),
    path('violation_comparator/', violation_comparator, name='violation_comparator'),
]
