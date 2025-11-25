"""
Exam and quiz models.
"""
from django.db import models
from django.utils import timezone
from accounts.models import User, Course


class Exam(models.Model):
    """Exam/Quiz model."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams', limit_choices_to={'role': 'teacher'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    max_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=40)
    is_published = models.BooleanField(default=False)
    allow_retake = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exams'
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['start_time', 'end_time']),
            models.Index(fields=['is_published']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.course.code}"
    
    @property
    def is_active(self):
        now = timezone.now()
        return self.is_published and self.start_time <= now <= self.end_time
    
    @property
    def is_upcoming(self):
        return self.is_published and timezone.now() < self.start_time
    
    @property
    def is_ended(self):
        return timezone.now() > self.end_time


class Question(models.Model):
    """Question model for exams."""
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='mcq')
    marks = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'questions'
        indexes = [
            models.Index(fields=['exam', 'order']),
        ]
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.order}"


class Option(models.Model):
    """Option model for MCQ questions."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'options'
        indexes = [
            models.Index(fields=['question', 'order']),
        ]
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question} - Option {self.order}"


class StudentAnswer(models.Model):
    """Student answer model."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_answers')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_answers', limit_choices_to={'role': 'student'})
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    answer_text = models.TextField(blank=True)
    selected_options = models.ManyToManyField(Option, blank=True, related_name='student_selections')
    marks_obtained = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'student_answers'
        unique_together = ['exam', 'student', 'question']
        indexes = [
            models.Index(fields=['exam', 'student']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.student.email} - {self.question}"


class AutoGradingResult(models.Model):
    """Auto-grading result model."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grading_results')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grading_results', limit_choices_to={'role': 'student'})
    total_marks_obtained = models.IntegerField(default=0)
    total_marks_possible = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_passed = models.BooleanField(default=False)
    graded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auto_grading_results'
        unique_together = ['exam', 'student']
        indexes = [
            models.Index(fields=['exam', 'student']),
            models.Index(fields=['student']),
        ]
        ordering = ['-graded_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.exam.title} - {self.percentage}%"

