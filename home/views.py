from django.shortcuts import render
from django.http import HttpResponse
from .models import ItParts
from .models import HomeItParts
from django.db.models import F
from django.shortcuts import render
import plotly.express as px
from core.forms import DateForm
from core.models import CO2

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')

def webpage1(request):
	
    return render(request, '../template/testPage.html')

def Home(request):
	
    return render(request, '../template/Home.html')

def Search(request):
   # LowSupply = ItParts.objects.raw(select name, from it_asset_parts.it_parts, where qty<=5)
  #  Manager.raw(select "name" as bar_label, count(*) as bar_quantity from it_asset_parts.it_parts as results group by "name" order by bar_quantity  desc)
    
    query = request.GET.get('search_res', None)
    #query2 = request.GET.get('Qty', None)
    context = {}    
    
    
    if query and request.method == 'GET':
     
        results = ItParts.objects.filter(barcode_rm=query)
        ItParts.objects.filter(barcode_rm=query).update(qty=F('qty')+1)
        context.update({'results': results})

        #query1 = 'UPDATE it_parts SET Qty = Qty + 1 WHERE Barcode_Add = 'query';'
   # if query and request.method == 'GET':
   #     results = ItParts.objects.filter(part_id=query)
   #     context.update({'results': results})
    #context = {
    #    'Parts_View': Parts_View
    #}
    return render(request, '../template/Search.html', context)


def Home(request):
    Parts_View = ItParts.objects.filter()
    query = request.GET.get('search_res', None)
    #query2 = request.GET.get('Qty', None)
    context = {'Parts_View': Parts_View}    
   # context1 = {'Parts_View': Parts_View}  
    
    if query and request.method == 'GET':
     
        results = ItParts.objects.filter(barcode_rm=query)
        results1 = ItParts.objects.filter(barcode_add=query)
        ItParts.objects.filter(barcode_rm=query).update(qty=F('qty')-1)
        ItParts.objects.filter(barcode_add=query).update(qty=F('qty')+1)
        #context.update({'results': results})
        context.update({'results': results, 'results1': results1} )

        #query1 = 'UPDATE it_parts SET Qty = Qty + 1 WHERE Barcode_Add = 'query';'
   # if query and request.method == 'GET':
   #     results = ItParts.objects.filter(part_id=query)
   #     context.update({'results': results})
    #context = {
    #    'Parts_View': Parts_View
    #}
    return render(request, '../template/Home.html', context)




def chart(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    co2 = CO2.objects.all()
    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        title="CO2 PPM",
        labels={'x': 'Date', 'y': 'CO2 PPM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, '../template/chart.html', context)