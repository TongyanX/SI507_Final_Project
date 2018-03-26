from django.shortcuts import render

# Create your views here.


def index(request):
    """Index Page"""
    return render(request, "index.html")


def table(request):
    """Table Page"""
    return render(request, "table.html")


def plot(request):
    """Plot Page"""
    return render(request, "plot.html")
