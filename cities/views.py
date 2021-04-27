from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from cities.forms import HtmlForm, CityForm
from cities.models import City

__all__ = (
    'home', 'CityDetailView', 'CityCreateView', 'CityUpdateView', 'CityDeleteView', 'CityListView',
)


def home(request, pk=None):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    # if pk:
    # city = City.objects.filter(id=pk).first()
    # city = City.objects.get(id=pk)
    # city = get_object_or_404(City, id=pk)
    #
    # context = {'object':city}
    # return render(request, 'cities/detail.html', context)
    form = HtmlForm()
    qs = City.objects.all()
    lst = Paginator(qs, 2)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy("cities: home")


class CityUpdateView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities: home')
    success_message = "Город успешно отредактирован"


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities: home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CityListView(ListView):
    paginate_by = 2
    model = City
    template_name = "cities/home.html"

    def get_context_data(self, **kwards):
        context = super().get_context_data(**kwards)
        form = CityForm()
        context['form'] = form
        return context
