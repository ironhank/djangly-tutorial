from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from polls.models import Poll, Choice

# def index(request):
# 	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
# 	template = loader.get_template('polls/index.html')
# 	context = RequestContext(request,
# 		{'latest_poll_list':latest_poll_list})
# 	return HttpResponse(template.render(context))

def index(request):
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	context = {'latest_poll_list':latest_poll_list}
	return render(request, 'polls/index.html', context)

def detail(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	return render(request, 'polls/detail.html', {'poll':poll})

def results(request, poll_id):
	return HttpResponse("You're looking at the results of poll %s" % poll_id)

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)

	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except KeyError, Choice.DoesNotExist:
		return render(request, 'polls/detail.html', {
			'poll':p,
			'error_message':"You didn't select a choice"
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponse(reverse('polls:results', args=(p.id,)))