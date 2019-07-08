from django.test import TestCase
from django.urls import reverse


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
