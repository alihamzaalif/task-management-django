from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

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
    