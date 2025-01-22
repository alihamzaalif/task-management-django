from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
# Create your views here.

def manager_dashboard(request):
    type = request.GET.get('type', 'all') #provides reply 'all' if nothing is provided
    # print(type)
    

    #getting task count
    # total_task = tasks.count()
    # completed_task = tasks.filter(status="COMPLETED").count()
    # in_progress_task = tasks.filter(status = "IN_PROGRESS").count()
    # pending_task = tasks.filter(status = "PENDING").count()
    
    # count = {
    #     "total_task":,
    #     "completed_task":,
    #     "in_progress_task":,
    #     "pending_task"
    # }
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed = Count('id', filter=Q(status="COMPLETED")),
        in_progress = Count('id', filter=Q(status="IN_PROGRESS")),
        pending = Count('id', filter=Q(status="PENDING")),
        )
    
    # Retriving task data
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()
    context = {
        "tasks" : tasks,
        "counts" : counts,
        # "total_task" : total_task,
        # "pending_task" : pending_task,
        # "in_progress_task" : in_progress_task,
        # "completed_task" : completed_task
    }
    return render(request,'dashboard/manager-dashboard.html', context)

def user_dashboard(request):
    return render(request,'dashboard/user-dashboard.html')


def create_task(request):
    # employees = Employee.objects.all()
    # form = TaskForm(employees=employees) #For GET
    task_form = TaskModelForm() #For GET
    task_detail_form = TaskDetailModelForm()

    # if request.method == "POST":
    #     form = TaskForm(request.POST,employees=employees)
    #     if form.is_valid():
    #         # print(form.cleaned_data)
    #         data = form.cleaned_data
    #         title = data.get('title')
    #         description = data.get('description')
    #         due_date = data.get('due_date')
    #         assigned_to = data.get('assigned_to')
    #         task = Task.objects.create(title=title, description=description, due_date=due_date)
    #         #Assign employee to task
    #         for emp_id in assigned_to:
    #             employee = Employee.objects.get(id=emp_id)
    #             task.assigned_to.add(employee)
            
    #         return HttpResponse("Task Added sucessfully")
    if request.method == "POST":
        task_form = TaskModelForm(request.POST) 
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model Form Data"""
            
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task created successfully")
            return redirect('create-task')
            # return render(request,'task_form.html',{"task_form":task_form, "task_detail_form":task_detail_form, "message": "task added successfully"})
            # print(form.cleaned_data)
            """ For Django Form data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')
            # task = Task.objects.create(title=title, description=description, due_date=due_date)
            # #Assign employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # 
            # return HttpResponse("Task Added sucessfully")
    context = {
        "task_form":task_form, "task_detail_form":task_detail_form
    }
    return render(request,"task_form.html",context)

def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) #For GET
    if task.details: 
        task_detail_form = TaskDetailModelForm(instance=task.details)
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task) 
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model Form Data"""
            
            task_form = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task updated successfully")
            return redirect('update-task',id)
    context = {
        "task_form":task_form, "task_detail_form":task_detail_form
    }
    return render(request,"task_form.html",context)

def delete_task(request,id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, "Something went wrong")
    return redirect('manager-dashboard')
def view_task(request):
    # # retrieve all data from task models
    # tasks = Task.objects.all()

    # # retrieve specific task
    # task3 = Task.objects.get(pk=1)

    # # fetch the first task
    # first_task = Task.objects.first()

    # pending_task = Task.objects.filter(status='PENDING')
    # completed_task = Task.objects.filter(status='COMPLETED')
    # today_pending = Task.objects.filter(due_date=date.today())

    # task_prty = TaskDetail.objects.exclude(priority="L")

    # return render(request, "show_task.html",{"tasks":tasks,"task3":task3,"first_task":first_task,"pending_task":pending_task,"completed_task":completed_task,"today_pending":today_pending,"task_prty":task_prty})

    # SHOW TASKS THAT CONTAIN THE LETTER C AND STATUS PENDING
    # tasks = Task.objects.filter(title__icontains="c",status="PENDING")

    #SHOW T HE TASSKS THAHT ARE PENDING OR IN-PROGRESS

    # tasks = Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS"))
    # tasks = Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS")).exists()
    # return render(request,'show_task.html',{"tasks":tasks})

    #  reverse related
    # tasks = Task.objects.select_related('details').all()
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all()

    # Prefetch Related {Reverse Foreignkey, many to many}
    # tasks = Project.objects.prefetch_related('task_set').all()
    tasks = Task.objects.prefetch_related('assigned_to').all()
    return render(request,"show_task.html",{"tasks":tasks})