from django.shortcuts import render

def home(request):
    return render(request, "info/index.html")

def about(request):
    return render(request, "info/about.html")

def schedule(request):
    return render(request, "info/schedule.html")

def sponsors(request):
    return render(request, "info/sponsors.html")

def rules(request):
    return render(request, "info/rules.html")
