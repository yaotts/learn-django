from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

import datetime

class QuestionModelTests(TestCase):

    def test_pub_recently_with_future_question(self):
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.pub_recently(),False)
    
    def test_pub_recently_with_old_question(self):
        time=timezone.now()-datetime.timedelta(days=3)
        old_question=Question(pub_date=time)
        self.assertIs(old_question.pub_recently(),False)

    def test_pub_recently_with_recent_question(self):
        time=timezone.now()-datetime.timedelta(hours=10)
        recent_question=Question(pub_date=time)
        self.assertIs(recent_question.pub_recently(),True)

def create_question(question_text,days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class IndexViewTests(TestCase):

    def test_no_question(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        create_question('past question',-5)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: past question>'])

    def test_future_question(self):
        create_question('future question',5)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_and_future_question(self):
        create_question('past question', -5)
        create_question('future question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: past question>'])
    
    def test_two_past_question(self):
        create_question('past question one', -5)
        create_question('past question two', -10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: past question two>','<Question: past question one>'])
    
class DetailViewTests(TestCase):

    def test_future_question(self):
        future_question=create_question('future question',5)
        url= reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question=create_question('past question',-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)









        
