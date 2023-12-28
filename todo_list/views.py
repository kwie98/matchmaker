from django.http import HttpResponse

from todo_list.models import Item


# Create your views here.
def index(request):
    return HttpResponse(b"Welcome to the todo list :)")


def items(request):
    items = Item.objects.all()
    return HttpResponse(items)


def item(request, item_id: int):
    try:
        item = Item.objects.get(id=item_id)
        return HttpResponse(f"{item}")
    except Exception as e:
        return HttpResponse(e)
