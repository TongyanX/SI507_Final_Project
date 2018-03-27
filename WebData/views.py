from django.shortcuts import render

# Create your views here.


def index(request):
    """Index Page"""
    return render(request, "index.html")


def table(request):
    """Table Page"""
    return render(request, "table.html")


def table_univ(request):
    """Table Page - University"""
    return render(request, "table_univ.html")


def table_gdp(request):
    """Table Page - GDP"""
    return render(request, "table_gdp.html")


def plot(request):
    """Plot Page"""
    return render(request, "plot.html")
