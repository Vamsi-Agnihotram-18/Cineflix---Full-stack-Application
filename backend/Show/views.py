from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Show
from .forms import ShowForm

def show_list(request):
    shows = Show.objects.all()
    return render(request, 'show_list.html', {'shows': shows})

class ShowCreateView(CreateView):
    model = Show
    form_class = ShowForm
    template_name = 'show_form.html'
    success_url = reverse_lazy('show_list')

class ShowUpdateView(UpdateView):
    model = Show
    form_class = ShowForm
    template_name = 'show_form.html'
    success_url = reverse_lazy('show_list')

class ShowDeleteView(DeleteView):
    model = Show
    template_name = 'show_confirm_delete.html'
    success_url = reverse_lazy('show_list')
