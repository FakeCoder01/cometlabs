from rest_framework import serializers
from .models import User, TestCase, Question
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_password(self, value: str) -> str:
        return make_password(value)

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['input', 'output']

class QuestionSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'test_cases']

    def create(self, validated_data):
        test_cases_data = validated_data.pop('test_cases')
        question = Question.objects.create(**validated_data)
        for test_case_data in test_cases_data:
            TestCase.objects.create(question=question, **test_case_data)
        return question
    
    def update(self, instance, validated_data):
        # Update the Question instance
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        # Delete existing TestCase instances
        TestCase.objects.filter(question=instance).delete()

        # Create new TestCase instances
        test_cases_data = validated_data.pop('test_cases')
        for test_case_data in test_cases_data:
            TestCase.objects.create(question=instance, **test_case_data)

        return instance
