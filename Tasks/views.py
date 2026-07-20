from django.shortcuts import render,redirect,get_object_or_404
from .models import Tasks
from django.utils import timezone
from .forms import TaskForm,CreateUserForm,LoginForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        
        form = CreateUserForm()   
         
    return render(request,'Tasks/register.html',{'form':form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            print("LOGIN SUCCESS:", user.username)

            login(request, user)

            print("CURRENT USER:", request.user)

            return redirect('home')
        else:
            print("LOGIN ERROR:", form.errors)

    else:
        form = LoginForm()

    return render(request, 'Tasks/login.html', {'form': form})

def logoutPage(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('loginpage')

@login_required(login_url='loginpage')
def home(request):
    task = Tasks.objects.filter(user=request.user,is_completed=False).order_by('-updated_at')
    completed_tasks = Tasks.objects.filter(user=request.user,is_completed=True)
    context = {
        'tasks':task,
        'completed':completed_tasks ,
        'now': timezone.now(),
    }
    return render(request,'Tasks/home-todo.html', context)

@login_required(login_url='loginpage')
def addTask(request):
    if request.method == "POST":
        task = request.POST.get('task')
        deadline = request.POST.get("deadline")

        Tasks.objects.create(user=request.user,task=task,deadline=deadline if deadline else None)
    return redirect('home')

@login_required(login_url='loginpage')
def mark_as_done(request, pk):
    task = get_object_or_404(Tasks, pk=pk,user=request.user)
    task.is_completed = True
    task.save()
    return redirect('home')

@login_required(login_url='loginpage')
def mark_as_undone(request, pk):
    task = get_object_or_404(Tasks, pk=pk,user=request.user)
    task.is_completed = False
    task.save()
    return redirect('home')

@login_required(login_url='loginpage')
def edit_task(request,pk):
    get_task = get_object_or_404(Tasks,pk=pk,user=request.user)
    if request.method == 'POST':
        get_task.task = request.POST.get('task')
        get_task.deadline = request.POST.get('deadline')
        get_task.save()
        return redirect('home')

    return render(request,'Tasks/edit_task.html',  {'get_task': get_task})

@login_required(login_url='loginpage')    
def delete_task(request,pk):

    task = get_object_or_404(Tasks, pk=pk,user=request.user)
    task.delete()
    return redirect('home')