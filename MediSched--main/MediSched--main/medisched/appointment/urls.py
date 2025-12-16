from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('book/<int:doctor_id>/', views.book_appointment, name='book'),
    path('payment/', views.payment_page, name='payment'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('confirmation/<int:appointment_id>/', views.appointment_confirmation, name='confirmation'),
    path('my-appointments/', views.appointment_list, name='list'),
    path('api/calculate-fees/', views.calculate_fees, name='calculate_fees'),
]