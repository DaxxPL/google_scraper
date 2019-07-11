from django.test import TestCase
from django.urls import reverse
from django_webtest import WebTest
from pytest_localserver.http import WSGIServer
import pytest
from urllib.parse import urlparse
import os
import requests



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

    def test_sending_filled_form_but_string_proxy(self):
        form = self.app.get(reverse('find')).form
        form['query'] = 'foo'
        form['proxy'] = 'bar'
        response = form.submit()
        self.assertContains(response, "Enter a valid IPv4 or IPv6 address.")

    def test_sending_filled_form_but_int_proxy(self):
        form = self.app.get(reverse('find')).form
        form['query'] = 'foo'
        form['proxy'] = 5412
        response = form.submit()
        self.assertContains(response, "Enter a valid IPv4 or IPv6 address.")

    def test_sending_filled_form_but_wrong_proxy(self):
        form = self.app.get(reverse('find')).form
        form['query'] = 'foo'
        form['proxy'] = '125,6.453,234'
        response = form.submit()
        self.assertContains(response, "Enter a valid IPv4 or IPv6 address.")

    def test_sending_vaild_form(self):
        import time
        form = self.app.get(reverse('find')).form
        form['query'] = 'foo'
        response = form.submit()
        print(response.url)
        time.sleep(7)
        print(requests.get('http://0.0.0.0:8000/search/foo').text)

