from django.shortcuts import render
from django.http import HttpResponse
from .engine.recengine import anime_recommendation
from .engine.dbConfig import animeConnect, ratingConnect

# Create your views here.
def home(request):    
   return render(request,"home.html",)


def search(request):
   if request.method == "POST":
      anime = request.POST['watched']
      try:
         recs = anime_recommendation(anime)
         context = {
            "list1": recs[0],
            "list2": recs[1],
            "anime": anime
         }
         return render(request,"recommendation.html",context)
      except:
         return HttpResponse('Did not find Anime')
   return render(request,"recommendation.html")
