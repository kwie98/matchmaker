from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "matchmaker/index.html")


def teams(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Team size: {request.POST['team_size']}")
