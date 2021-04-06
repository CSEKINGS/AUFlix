from django.shortcuts import render

# Create your views here.
class Videopage:
    def videos(request):
        return render(request,'videos.html')