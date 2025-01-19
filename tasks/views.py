from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
# Create your views here.
def home(request):
    # Work with database
    # Transform data
    # Data pass
    # http response / json response
    # return HttpResponse("Welcome to the task management system")
    return render(request,"home.html")

def contact(request):
    return HttpResponse("<h1 style='color: red'>Welcome to the contact page</h1>")

def show_task(request):
    return HttpResponse("This is our task page")

def show_specific_task(request,id):
    print("id ", id)
    print("id type ", type(id))
    return HttpResponse(f"This is our dynamic task page {id}")

def manager_dashboard(request):
    return render(request,'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request,'dashboard/user-dashboard.html')

def test(request):
    context = {
        "names": ["Mahmud","Ahamed","John","Hamza"],
        "age": 23
    }
    return render(request,'test.html',context)

def create_task(request):
    employees = Employee.objects.all()
    # form = TaskForm(employees=employees) #For GET
    form = TaskModelForm() #For GET

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
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model Form Data"""
            print(form)
            form.save()
            return render(request,'task_form.html',{"form":form,"message": "task added successfully"})
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
        "form":form
    }
    return render(request,"task_form.html",context)

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