from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, TitleViewSet, UserRegistration, UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserRegistration.as_view()),
    #path('v1/auth/token/',.....................as_view()),

]