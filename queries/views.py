from django.shortcuts import render, redirect, HttpResponse
from django import views
from .models import Query
from .forms import SearchForm
from .tasks import process_data
from django.core.exceptions import ObjectDoesNotExist


class SearchView(views.View):

    def get(self, request, pk):
        try:
            item = Query.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return render(request, 'queries/query_wrong.html', {'pk': pk})
        return render(request, 'queries/query_detail.html', {'object': item})


class QueryView(views.View):
    form_class = SearchForm

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request):
        form = self.form_class
        return render(request, 'queries/query_form.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        query = form.data['query']
        timeout = form.data['timeout']
        client_ip = self.get_client_ip(request)
        try:
            timeout = float(timeout)
        except ValueError:
            timeout = 0
        process_data.s(query, client_ip).apply_async(soft_time_limit=timeout)
        return redirect(f'/search/{query}')
