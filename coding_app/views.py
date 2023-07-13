from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, QuestionSerializer, TestCaseSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, TestCase, Question
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "email": user.email,
                "token": str(RefreshToken.for_user(user).access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            return Response({
                "email": user.email,
                "token": str(RefreshToken.for_user(user).access_token)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Wrong email or password"}, status=status.HTTP_400_BAD_REQUEST)


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


    def update1(self, instance, validated_data):
        test_cases_data = validated_data.pop('test_cases')
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        TestCase.objects.filter(question=instance).delete()
        for test_case_data in test_cases_data:
            TestCase.objects.create(question=instance, **test_case_data)
        return instance



    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Question.objects.all()
        return Question.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class SolutionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, question_id):
        question = Question.objects.get(id=question_id)
        solution = request.data.get('solution')

        # Call Sphere Engine API here with the solution and the test cases
        # Parse the response and return it

        return Response({"message": "Solution submitted"}, status=status.HTTP_200_OK)
    

