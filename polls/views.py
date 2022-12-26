# raising a 404 erorr
# from django.http import Http404

from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
# generic view for less code
from django.views import generic 

# from django.template import loader

from .models import Question, Choice 


# def index(request):
#     last_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in last_question_list])
#     return HttpResponse(output)

# use tempates
# def index(request):
#     # query data from database
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # render() load a template
#     return render(request, 'polls/index.html', context)

# Http404 Erorr
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404('Question does not exist')
#     return render(request, 'polls/detail.html', {'question': question})

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        # If two users vote the same time, this might go wrong.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })      
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Alway return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a 
        # user hits the Back buttun.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

from django.utils import timezone

# generic view for less code
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions. 
        (not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question 
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any question that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
