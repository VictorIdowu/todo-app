from django.shortcuts import render,redirect
from .models import Task
from .forms import TodoForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.

class TaskListView(ListView):
  model = Task
  template_name = 'myapp/index.html'
  context_object_name = 'task_list'

def index(request):
  task_list = Task.objects.all()
 
  return render(request,'myapp/index.html', {
    'task_list':task_list
  })

def add(request):
  if request.method == 'POST':
    name = request.POST.get('name', '')
    priority = request.POST.get('priority', '')
    date = request.POST.get('date', '')

    task = Task(name=name,priority=priority,date=date)
    task.save()
    return redirect('/')

  return render(request,'myapp/add.html')



def delete(request, taskid):
  task = Task.objects.get(id=taskid)

  if request.method == 'POST':
    task.delete()
    return redirect('/')

  return render(request, 'myapp/delete.html', {
    'task':task
  })

class TaskUpdateView(UpdateView):
  model = Task
  template_name = 'myapp/edit.html'
  context_object_name = 'task'
  fields = {'name','priority','date'}

  def get_success_url(self):
    return reverse_lazy('cbvindex')


def update(request, taskid):
  task = Task.objects.get(id=taskid)
  form = TodoForm(request.POST or None, instance=task)

  if form.is_valid():
    form.save()
    return redirect('/')
  
  return render(request, 'myapp/edit.html', {'form':form, 'task':task})