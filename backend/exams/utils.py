"""
Exam utilities for auto-grading.
"""
from .models import StudentAnswer, AutoGradingResult, Question


def auto_grade_exam(exam, student):
    """
    Auto-grade an exam for a student.
    Returns grading result.
    """
    student_answers = StudentAnswer.objects.filter(exam=exam, student=student)
    total_marks_obtained = 0
    total_marks_possible = 0
    
    for answer in student_answers:
        question = answer.question
        total_marks_possible += question.marks
        
        if question.question_type == 'mcq':
            # Check if selected options match correct options
            correct_options = question.options.filter(is_correct=True)
            selected_options = answer.selected_options.filter(is_correct=True)
            
            if correct_options.count() == selected_options.count() and \
               set(correct_options.values_list('id', flat=True)) == set(selected_options.values_list('id', flat=True)):
                answer.is_correct = True
                answer.marks_obtained = question.marks
                total_marks_obtained += question.marks
            else:
                answer.is_correct = False
                answer.marks_obtained = 0
        else:
            # For short/long answer, mark as ungraded (needs manual grading)
            answer.is_correct = None
            answer.marks_obtained = None
        
        answer.save()
    
    # Calculate percentage
    percentage = (total_marks_obtained / total_marks_possible * 100) if total_marks_possible > 0 else 0
    is_passed = percentage >= exam.passing_marks
    
    # Create or update grading result
    result, created = AutoGradingResult.objects.get_or_create(
        exam=exam,
        student=student,
        defaults={
            'total_marks_obtained': total_marks_obtained,
            'total_marks_possible': total_marks_possible,
            'percentage': percentage,
            'is_passed': is_passed,
        }
    )
    
    if not created:
        result.total_marks_obtained = total_marks_obtained
        result.total_marks_possible = total_marks_possible
        result.percentage = percentage
        result.is_passed = is_passed
        result.save()
    
    return {
        'total_marks_obtained': total_marks_obtained,
        'total_marks_possible': total_marks_possible,
        'percentage': float(percentage),
        'is_passed': is_passed,
    }

