from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

class PollMethodTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		# should return false for polls whose pub_date is in the future
		future_poll = Poll(pub_date = timezone.now() + datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_old_poll(self):
		# should return false for polls whose pub_date is in the future
		future_poll = Poll(pub_date = timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_recent_poll(self):
		# should return false for polls whose pub_date is in the future
		future_poll = Poll(pub_date = timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(future_poll.was_published_recently(), True)


def create_poll(question, days):
	return Poll.objects.create(question=question,pub_date=timezone.now()+datetime.timedelta(days))

class PollViewTest(TestCase):
	def test_index_view_with_no_polls(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])
	
	def test_index_view_with_past_poll(self):
		create_poll(question="past Poll",days = -30)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: past Poll>'])

	def test_index_view_with_a_future_poll(self):
		create_poll(question="future Poll",days = 10)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_two_past_polls(self):
		create_poll(question="past poll 30",days = -30)
		create_poll(question="past poll 3",days = -3)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: past poll 3>','<Poll: past poll 30>'])

	def test_index_view_with_past_poll_and_future_poll(self):
		create_poll(question="past Poll",days = -30)
		create_poll(question="future Poll",days = 10)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: past Poll>'])


class PollIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_poll(self):
		future_poll = create_poll(question="Future Poll", days=5)
		response = self.client.get(reverse('polls:detail',args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll(self):
		past_poll = create_poll(question="Past Poll", days=-5)
		response = self.client.get(reverse('polls:detail',args=(past_poll.id,)))
		self.assertContains(response, past_poll.question, status_code=200)



