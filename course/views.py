from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def vue_test(request: HttpRequest) -> HttpResponse:
    return render(request, 'course/test.html')
