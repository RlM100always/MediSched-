from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

# Root URL view
def root_view(request):
    return HttpResponse("<h1>Welcome to MediSched Root Page!</h1>")

def home_view(request):
    return HttpResponse("<h1>Welcome to Home Page!</h1>")


def work_view(request):
    return HttpResponse("<h1>Welcome to Work Page!</h1>")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Home app
    path('users/', include('users.urls', namespace='users')),  # ajax endpoints + dashboards
    path('users/doctor/', include('doctor.urls', namespace='doctor')),


    
]

