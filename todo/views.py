from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime


def create_todo(request):
    message = ""
    form = TodoForm()
    if request.method == "POST":
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            message = "建立事項成功"

            return redirect("todolist")
        except Exception as e:
            print(e)
            message = "建立事項失敗..."

    return render(request, "todo/create-todo.html", {"form": form, "message": message})


# Create your views here.
def todolist(request):
    # all,get,filter
    # todos = Todo.objects.all()
    todos = None
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user).order_by("-created")

    return render(request, "todo/todo.html", {"todos": todos})


def view_todo(request, id):
    todo = None
    message = ""
    try:
        todo = Todo.objects.get(id=id)
        form = TodoForm(instance=todo)

        if request.method == "POST":
            print(request.POST)
            if request.POST.get("update"):
                todo.date_completed = (
                    datetime.now() if request.POST.get("completed") else None
                )

                form = TodoForm(request.POST, instance=todo)
                if form.is_valid():
                    form.save()
                    message = "修改成功"
            elif request.POST.get("delete"):
                todo.delete()
                return redirect("todolist")

    except Exception as e:
        print(e)
        message = "修改或刪除失敗..."

    return render(request, "todo/view-todo.html", {"todo": todo, "form": form})
