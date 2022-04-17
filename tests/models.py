from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    point = models.PositiveIntegerField()
    test = models.ForeignKey('Test', on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Sphere(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

test_complexity = (
    (1, 'hard'),
    (2, 'normal'),
    (3, 'easy')
)

def get_slug():
    code = get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return code

class Test(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    sphere = models.ManyToManyField(Sphere, blank=True)
    complexity = models.PositiveIntegerField(choices=test_complexity)
    slug = models.SlugField(default=get_slug)


    def __str__(self):
        return self.name

    def get_questions(self):
        q = Question.objects.filter(test=self.pk).values('question', 'answer', 'point', 'pk')
        return q
