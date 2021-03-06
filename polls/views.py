from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import DetailView, TemplateView

from .models import Question, Choice


class IndexView(TemplateView):
    """ Poll index view
    """
    template_name = 'polls/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_question_list'] = Question.objects.order_by('-pub_date')[:5]
        return context


class DetailView(TemplateView):
    """ Polls details view
    """
    template_name = 'polls/details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(id=kwargs['question_id'])
        return context


class ResultView(TemplateView):
    """ Poll results view
    """
    template_name = 'polls/results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(id=kwargs['question_id'])
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
