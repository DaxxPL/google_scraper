from celery.task.control import inspect
from django import views
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django_celery_results.models import TaskResult

from .forms import SearchForm
from .models import Query
from .tasks import process_data


class SearchView(views.View):

    def get(self, request, pk):
        pk = pk.lower()
        i = inspect()
        active = i.active()
        for item in active[list(active)[0]]:
            if item['args'].startswith(f"('{pk}'"):
                return render(request, 'queries/query_progress.html', {'object': item})
        try:
            item = Query.objects.get(pk=pk)
            return render(request, 'queries/query_detail.html', {'object': item})
        except ObjectDoesNotExist:
            try:
                task_result = TaskResult.objects.filter(task_args__startswith=f"('{pk}'").order_by('-date_done')[0]
                return render(request, 'queries/query_failed.html', {'object': task_result})
            except IndexError:
                return render(request, 'queries/query_wrong.html', {'pk': pk})


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
        if form.is_valid():
            query = form.data['query'].lower()
            timeout = form.data['timeout']
            browser = form.data['browser']
            proxy = form.cleaned_data['proxy']
            try:
                timeout = float(timeout)
            except ValueError:
                timeout = 0
            client_ip = self.get_client_ip(request)
            process_data.s(query, client_ip, browser, proxy).apply_async(soft_time_limit=timeout)
            return redirect(f'/search/{query}')
        else:
            return render(request, 'queries/query_form.html', {'form': form})
