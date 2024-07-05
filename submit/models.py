from django.db import models
from problems.models import Problem  # Import the Problem model from your problems app

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),
    ("cpp", "C++"),
]

class CodeSubmission(models.Model):
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    input_data = models.TextField(null=True, blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"CodeSubmission {self.id}"
