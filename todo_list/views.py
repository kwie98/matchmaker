from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from todo_list.models import Item


# Create your views here.
def index(_: HttpRequest) -> HttpResponse:
    return HttpResponse("Welcome to the todo list :)")


def items(request: HttpRequest) -> HttpResponse:
    return render(request, "todo_list/items.html", {"items": Item.objects.all()})


def item(_: HttpRequest, item_id: int) -> HttpResponse:
    try:
        item = Item.objects.get(id=item_id)
        return HttpResponse(f"{item}")
    except Exception as e:
        return HttpResponse(e)
