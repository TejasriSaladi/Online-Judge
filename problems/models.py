from django.db import models

class Problem(models.Model):
    statement = models.TextField(blank=True, default='General')
    name = models.CharField(max_length=5000)
    unique_id = models.CharField(max_length=50, unique=True)
    level = models.CharField(
        max_length=10,
        blank=True,
        choices=[
            ("Hard", "Hard"),
            ("Easy", "Easy"),
            ("Medium", "Medium"),
        ],
    )
    topic = models.CharField(max_length=100, default='General')
    input_format = models.TextField(blank=True, default='General')
    output_format = models.TextField(blank=True, default='General')
    constraints = models.TextField(blank=True, default='No constraints')
    

    def __str__(self):
        return self.name

    
class TestCase(models.Model):
    input = models.TextField(blank=True, default=None)
    output = models.TextField(blank=True, default=None)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Test case for {self.problem.name}"

    
class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=100, blank=True, null=True) 
    submitted_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f"Solution for {self.problem.name}"
