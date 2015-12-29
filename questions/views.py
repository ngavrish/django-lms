from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from courses.models import Course
from courses.views import teacher_check
from questions.forms import QuestionForm, ChoiceForm
from questions.models import Question, Choice

def update(question_form, question, choice_formset):
	question.name = question_form.cleaned_data['name']
	question.question_text = question_form.cleaned_data['question_text']
	question.save()
	for choice_form in choice_formset.forms:
		choice = choice_form.save(commit=False)
		choice.question = question
		choice.save()	

@user_passes_test(teacher_check)
def create_question(request, course_id):
	ChoiceFormSet = modelformset_factory(Choice, ChoiceForm, extra=4)
	course = Course.objects.get(id=course_id)
	if request.method == 'POST':			
		question_form = QuestionForm(data=request.POST)
		choice_formset = ChoiceFormSet(data=request.POST)
		if question_form.is_valid() and choice_formset.is_valid():	
			question = question_form.save(commit=False)
			question.owner = request.user
			question.course = course
			question.save()
			for choice_form in choice_formset.forms:
				choice = choice_form.save(commit=False)
				choice.question = question
				choice.save()	
			return redirect('/courses/' + course_id)
	else:
		question_form = QuestionForm()
		choice_formset = ChoiceFormSet(queryset=Choice.objects.none())
	return render(request, 'create_question.html', {'form': question_form, 'choice_formset': choice_formset, 
		'course': course })

@user_passes_test(teacher_check)
def edit_question(request, course_id, question_id):
	ChoiceFormSet = modelformset_factory(Choice, ChoiceForm, extra=0)
	course = Course.objects.get(id=course_id)
	question = Question.objects.get(id=question_id)
	choices = Choice.objects.filter(question=question)
	if request.user.username == question.owner:
		if request.method == 'POST' and 'update' in request.POST:
			question_form = QuestionForm(instance=question, data=request.POST)
			choice_formset = ChoiceFormSet(data=request.POST)
			if question_form.is_valid() and choice_formset.is_valid():
				Choice.objects.filter(question=question).delete()	
				update(question_form, question, choice_formset)
				return redirect('/courses/' + course_id)						
		if request.method == 'POST' and 'delete' in request.POST:
			question.delete()
			Choice.objects.filter(question=question).delete()		
			return redirect('/courses/' + course_id)		
		else:
			question_form = QuestionForm(instance=question)
			choice_formset = ChoiceFormSet(queryset=Choice.objects.filter(question=question))
		return render(request, 'edit_question.html', {'form': question_form, 'choice_formset': choice_formset,
			'course': course, 'question': question, 'choices': choices })
	return redirect('/courses/' + course_id)