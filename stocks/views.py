from django.shortcuts import render, redirect
from .models import *
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_3e7a40ff1263447fad36b733c43c2d6e&period=annual")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "ERROR..."
        return render(request, 'stocks/home.html', {'api': api})

    else:
        return render(request, 'stocks/home.html', {'ticker': "Enter a Ticker Above..."})



def about(request):
    return render(request, 'stocks/about.html', {})

def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []

        for tick in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(tick) + "/quote?token=pk_3e7a40ff1263447fad36b733c43c2d6e&period=annual")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "ERROR..."

        return render(request, 'stocks/add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(add_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'stocks/delete_stock.html', {'ticker': ticker})