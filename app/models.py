from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_questions_solved = models.PositiveIntegerField(default=0)
    total_correct_answers = models.PositiveIntegerField(default=0)

    def calculate_average_correct(self):
        if self.total_questions_solved == 0:
            return 0
        return (self.total_correct_answers / self.total_questions_solved) * 100

    def __str__(self):
        return f"{self.user.username}"


class ModeratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    LANGUAGE_CHOICES = [
        ('cro', 'Croatian'),
        ('eng', 'English'),
        ('ger', 'German'),
    ]
    lang = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='eng')

    def __str__(self):
        return f"{self.user.username}"


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('YN', 'Yes/No'),
        ('MC', 'Multiple Choice'),
    ]
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
    )
    LANGUAGE_CHOICES = [
        ('cro', 'Croatian'),
        ('eng', 'English'),
        ('ger', 'German'),
    ]
    lang = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='eng')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} ({self.lang})"


class YesNoQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_option = models.CharField(max_length=5, default='True', choices=[
        ('True', 'True'),
        ('False', 'False'),
    ])

    def __str__(self):
        return f"Yes/No: {self.question.text}"


class MultipleChoiceQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, default='A', choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])

    def __str__(self):
        return f"Multiple Choice: {self.question.text}"


class QuestionAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    shown_at = models.DateTimeField(default=now)
    solved_at = models.DateTimeField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    selected_option = models.CharField(max_length=5, null=True, blank=True)

    def time_taken(self):
        if self.solved_at:
            return (self.solved_at - self.shown_at).total_seconds()
        return None

    def __str__(self):
        return f"{self.user.username} - {self.question.text} ({'Correct' if self.is_correct else 'Incorrect'})"
