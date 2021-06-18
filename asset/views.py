from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Balance,Category
from .forms import BalanceForm

from django.db.models import Q

class BalanceView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        categories  = Category.objects.all()

        if "search" in request.GET:

            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("asset:index")

            search      = request.GET["search"].replace(" ","　")
            search_list =search.split(" ")

            query       = Q()
            for word in search_list:

                query &= Q(title__contains=word)

            balances  = Balance.objects.filter(query)
        else:
            balances  = Balance.objects.all()


        balances      = list(balances.values())


        total       = 0
        for balance in balances:

            total          = total + int(balance["income"]) - int(balance["spending"])
            balance["total"] = total

            if balance["category_id"]:
                category            = Category.objects.filter(id=balance["category_id"]).first()
                balance["category"] = category.name

        context = { "balances":balances,
                    "categories":categories,
                   }

        return render(request,"asset/index.html",context)

    def post(self, request, *args, **kwargs):

        form = BalanceForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("asset:index")

index   = BalanceView.as_view()

class BalanceDeleteView(LoginRequiredMixin,View):

    def post(self,request, pk, *args, **kwargs):

        balance = Balance.objects.filter(id=pk).first()
        balance.delete()

        return redirect("asset:index")

delete = BalanceDeleteView.as_view()

