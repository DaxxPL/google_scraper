from django.test import TestCase
from django.urls import reverse
from django_webtest import WebTest


class SearchViewTest(TestCase):

    def test_view_index_page_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('find'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('find'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'queries/query_form.html')


class SearchViewFormTest(WebTest):

    def test_sending_not_filled_form(self):
        form = self.app.get(reverse('find')).form
        response = form.submit()
        self.assertContains(response, "This field is required.")

    def test_sending_filled_form_but_negative_number_timeout(self):
        form = self.app.get(reverse('find')).form
        form['query'] = 'foo'
        form['timeout'] = -4
        response = form.submit()
        self.assertContains(response, "Ensure this value is greater than or equal to 0.0")

    def test_sending_filled_form_but_string_timeout(self):
        form = self.app.get(reverse('find')).form
        form['query'] = 'foo'
        form['timeout'] = 'bar'
        response = form.submit()
        self.assertContains(response, "Enter a number.")
