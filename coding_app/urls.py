from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, LoginView, QuestionViewSet, SolutionView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('solution/<int:question_id>/', SolutionView.as_view(), name='solution'),
    path('', include(router.urls)),
]
