"""
Serializers for exams app.
"""
from rest_framework import serializers
from .models import Exam, Question, Option, StudentAnswer, AutoGradingResult
from accounts.serializers import CourseSerializer, UserSerializer


class OptionSerializer(serializers.ModelSerializer):
    """Option serializer."""
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer."""
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_at',)


class ExamSerializer(serializers.ModelSerializer):
    """Exam serializer."""
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    teacher_name = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True, read_only=True)
    is_active = serializers.SerializerMethodField()
    is_upcoming = serializers.SerializerMethodField()
    is_ended = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'teacher')
    
    def get_teacher_name(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}" if obj.teacher else None
    
    def get_is_active(self, obj):
        return obj.is_active
    
    def get_is_upcoming(self, obj):
        return obj.is_upcoming
    
    def get_is_ended(self, obj):
        return obj.is_ended


class StudentAnswerSerializer(serializers.ModelSerializer):
    """Student answer serializer."""
    question = QuestionSerializer(read_only=True)
    question_id = serializers.IntegerField(write_only=True)
    selected_options = OptionSerializer(many=True, read_only=True)
    selected_option_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = StudentAnswer
        fields = '__all__'
        read_only_fields = ('submitted_at', 'student', 'marks_obtained', 'is_correct')
    
    def create(self, validated_data):
        selected_option_ids = validated_data.pop('selected_option_ids', [])
        answer = StudentAnswer.objects.create(**validated_data)
        if selected_option_ids:
            answer.selected_options.set(selected_option_ids)
        return answer


class AutoGradingResultSerializer(serializers.ModelSerializer):
    """Auto-grading result serializer."""
    student = UserSerializer(read_only=True)
    exam = ExamSerializer(read_only=True)
    
    class Meta:
        model = AutoGradingResult
        fields = '__all__'
        read_only_fields = ('graded_at',)

