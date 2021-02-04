from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import TaskForm
from .models import Task


class CreateTask(LoginRequiredMixin, CreateView):

    model = Task
    template_name = 'task_create.html'
    fields = ('title', 'body')
    login_url = 'login'

    def form_valid(self, form):

        form.instance.author = self.request.user
        form.instance.active = True
        return super().form_valid(form)


@login_required(login_url='login')
def ListTask(request):

    template_name = 'task_list.html'
    id = request.user.id
    tasks = Task.objects.filter(author=id, active=True).order_by('-date')
    if request.method == 'POST':
        obj = get_object_or_404(Task, id=request.POST.get('id'))
        obj.active = False
        obj.save()
        return HttpResponseRedirect(reverse('task_list'))
    else:
        new_form = TaskForm()
    context = {
        'form': new_form,
        'tasks': tasks,
    }
    return render(request, template_name, context)


class UpdateTask(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Task
    template_name = 'task_update.html'
    fields = ('title', 'body')
    login_url = 'login'

    def test_func(self):

        obj = self.get_object()
        return obj.author == self.request.user


class DeleteTask(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TaskCompleted(LoginRequiredMixin, ListView):

    template_name = 'task_completed.html'
    model = Task
    login_url = 'login'

    def get_queryset(self):

        return Task.objects.filter(author=self.request.user.id, active=False).order_by('-date')

    def post(self, request, *args, **kwargs):

        obj = get_object_or_404(Task, id=request.POST.get('id'))
        obj.active = True
        obj.save()
        return HttpResponseRedirect(reverse('task_completed'))



