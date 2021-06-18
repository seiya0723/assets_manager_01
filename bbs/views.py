from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Topic,Category
from .forms import TopicForm

from django.db.models import Q

class BbsView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        categories  = Category.objects.all()

        if "search" in request.GET:

            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("bbs:index")

            search      = request.GET["search"].replace(" ","　")
            search_list =search.split(" ")

            query       = Q()
            for word in search_list:

                query &= Q(title__contains=word)


            topics  = Topic.objects.filter(query)
        else:
            topics  = Topic.objects.all()


        topics      = list(topics.values())


        total       = 0
        for topic in topics:

            total          = total + int(topic["income"]) - int(topic["spending"])
            topic["total"] = total

            if topic["category_id"]:
                category            = Category.objects.filter(id=topic["category_id"]).first()
                topic["category"]   =category.name


        chobos = []
        context = {"chobos":chobos,
                   "balances":topics,
                   "categories":categories,
                   }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        form = TopicForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("bbs:index")

index   = BbsView.as_view()

class BbsDeleteView(LoginRequiredMixin,View):

    def post(self,request, pk, *args, **kwargs):

        topic = Topic.objects.filter(id=pk).first()
        topic.delete()

        return redirect("bbs:index")

delete = BbsDeleteView.as_view()

# Create your views here.
