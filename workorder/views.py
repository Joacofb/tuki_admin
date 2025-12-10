from django.shortcuts import render

# Create your views here.
def workorder(request):

    return render(request, 'workorder/workorder.html')