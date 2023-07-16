from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('participant', 'Participant'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)


class Question(models.Model):
    text = models.TextField()
    sphere_problem_id = models.BigIntegerField(null=True, blank=True)
    def __str__(self) -> str:
        return self.text

class TestCase(models.Model):
    question = models.ForeignKey(Question, related_name='test_cases', on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()

    def __str__(self) -> str:
        return self.question.text
