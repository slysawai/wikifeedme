# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
import time
import gourmand

def index(request):
    template = loader.get_template('wikifeedme/index.html')
    return HttpResponse(template.render(Context()))

def feedMe(request):
    template = loader.get_template('wikifeedme/fuetterung.html')
    randomMenu = gourmand.spitItOut()
    context = Context({
            'starterUrl': randomMenu[0][1],
            'starterName': randomMenu[0][2],
            'mainCourseUrl': randomMenu[1][1],
            'mainCourseName': randomMenu[1][2],
            'dessertUrl': randomMenu[2][1],
            'dessertName': randomMenu[2][2],
            'randomNumber': time.time(),
        })
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('wikifeedme/about.html')
    return HttpResponse(template.render(Context()))
