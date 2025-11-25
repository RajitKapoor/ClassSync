"""
Views for exams app.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Exam, Question, Option, StudentAnswer, AutoGradingResult
from .serializers import ExamSerializer, QuestionSerializer, StudentAnswerSerializer, AutoGradingResultSerializer
from .utils import auto_grade_exam


class IsTeacherOrReadOnly(permissions.BasePermission):
    """Permission to allow only teachers to create/edit exams."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_teacher


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet for exams."""
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Exam.objects.filter(teacher=user)
        elif user.is_student:
            return Exam.objects.filter(course__students=user, is_published=True)
        elif user.is_admin:
            return Exam.objects.all()
        return Exam.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit exam answers (student only)."""
        if not request.user.is_student:
            return Response({'error': 'Only students can submit exams.'}, status=status.HTTP_403_FORBIDDEN)
        
        exam = self.get_object()
        
        if not exam.is_published:
            return Response({'error': 'Exam is not published.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() < exam.start_time:
            return Response({'error': 'Exam has not started yet.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > exam.end_time:
            return Response({'error': 'Exam has ended.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already submitted
        if not exam.allow_retake and StudentAnswer.objects.filter(exam=exam, student=request.user).exists():
            return Response({'error': 'Exam already submitted.'}, status=status.HTTP_400_BAD_REQUEST)
        
        answers_data = request.data.get('answers', [])
        
        # Save answers
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            answer_text = answer_data.get('answer_text', '')
            selected_option_ids = answer_data.get('selected_option_ids', [])
            
            try:
                question = Question.objects.get(id=question_id, exam=exam)
            except Question.DoesNotExist:
                continue
            
            student_answer, created = StudentAnswer.objects.get_or_create(
                exam=exam,
                student=request.user,
                question=question,
                defaults={
                    'answer_text': answer_text,
                }
            )
            
            if selected_option_ids:
                student_answer.selected_options.set(selected_option_ids)
                student_answer.answer_text = answer_text
                student_answer.save()
        
        # Auto-grade
        result = auto_grade_exam(exam, request.user)
        
        return Response({
            'message': 'Exam submitted successfully.',
            'result': result
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get exam results."""
        exam = self.get_object()
        
        if request.user.is_student:
            # Student can only see their own results
            result = AutoGradingResult.objects.filter(exam=exam, student=request.user).first()
            if result:
                return Response(AutoGradingResultSerializer(result).data)
            return Response({'message': 'Results not available yet.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.is_teacher or request.user.is_admin:
            # Teacher/admin can see all results
            results = AutoGradingResult.objects.filter(exam=exam)
            return Response(AutoGradingResultSerializer(results, many=True).data)
        
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for questions."""
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]
    
    def get_queryset(self):
        exam_id = self.request.query_params.get('exam_id')
        if exam_id:
            return Question.objects.filter(exam_id=exam_id)
        return Question.objects.none()
    
    def perform_create(self, serializer):
        exam_id = self.request.data.get('exam_id')
        if exam_id:
            from .models import Exam
            exam = Exam.objects.get(id=exam_id)
            if exam.teacher != self.request.user:
                raise permissions.PermissionDenied("You can only add questions to your own exams.")
            serializer.save(exam=exam)

