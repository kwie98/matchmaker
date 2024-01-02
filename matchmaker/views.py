from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """Display a form to input team size and players."""
    return render(request, "matchmaker/index.html")


def make_teams(request: HttpRequest) -> HttpResponse:
    """Show generated teams and give the option of re-rolling or going back."""
    # TODO Validate user input
    # TODO Save input in session?
    return HttpResponseRedirect(reverse("matchmaker:teams"))

def teams(request: HttpRequest) -> HttpResponse:
    return HttpResponse("I can't access the input :(")
