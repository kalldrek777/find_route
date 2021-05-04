from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from routes.forms import RouteForm
from routes.models import Route
from routes.utils import get_routes


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})

def find_routes(request):
     if request.method == 'POST':
         form = RouteForm(request.POST)
         if form.is_valid():
             try:
                context = get_routes(request, form)
             except ValueError as e:
                 messages.error(request, e)
                 return render(request, 'routes/home.html', {'form': form})
             return render(request, 'routes/home.html', context)
         return render(request, 'routes/home.html', {'form': form})
     else:
         form = RouteForm()
         messages.error(request, 'Нет данных для поиска')
         return render(request, 'routes/home.html', {'form': form})


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален')
        return self.post(request, *args, **kwargs)
