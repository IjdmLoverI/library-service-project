from rest_framework import routers
from django.urls import path, include

from books import views

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "books"
