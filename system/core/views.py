from django.shortcuts import render

# Create your views here.

#@login_required
def index(request):
    context = {'message':'ok'}
    return render(request, 'templates/index.html', context)