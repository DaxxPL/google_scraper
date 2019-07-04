from django.shortcuts import render, redirect
from django import views
from .models import Query
from .forms import SearchForm


class QueryView(views.generic.CreateView):
    model = Query
    fields = ('text', )


class SearchView(views.generic.DetailView):
    model = Query


class MyView(views.View):

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
        q = Query()
        q.text = query
        q.client_ip = self.get_client_ip(request)
        q.save()
        return redirect(q.get_absolute_url())
