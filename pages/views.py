from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import NewQuestionForm, NewResponseForm, NewReplyForm

@login_required(login_url='/account/login')
def newQuestionPage(request):
    form = NewQuestionForm()
    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                return redirect('question', id=question.id)
        except Exception as e:
            print(e)
            raise
    context = {'form': form}
    return render(request, 'new-question.html', context)

def homePage(request):
    questions = Question.objects.all().order_by('-created_at')
    context = {
        'questions': questions
    }
    return render(request, 'homepage.html', context)

def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()
    question = get_object_or_404(Question, id=id)

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = question
                response.save()
                return redirect('question', id=id)
        except Exception as e:
            print(e)
            raise

    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'question.html', context)

@login_required(login_url='/account/login')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = get_object_or_404(Question, id=question_id)
                reply.parent = get_object_or_404(Response, id=parent_id)
                reply.save()
                return redirect('question', id=question_id)
        except Exception as e:
            print(e)
            raise
    return redirect('forum')

@login_required(login_url='/account/login')
def like_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    if request.user in response.likes.all():
        response.likes.remove(request.user)
    else:
        response.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))