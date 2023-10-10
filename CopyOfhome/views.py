from django.shortcuts import render
from django.http import HttpResponse
from .models import ItParts, HomeItParts, InventoryChange
from django.db.models import F
from django.shortcuts import render
import plotly.express as px
from core.forms import DateForm
import json
from django.db.models import IntegerField
from django.db.models.functions import Cast
from ipware import get_client_ip
from django.db.models import Q


# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')


def webpage1(request):
	
    return render(request, '../template/testPage.html')



def low_quantity_parts(request):
    low_quantity_parts = ItParts.objects.annotate(int_qty=Cast('qty', IntegerField())).filter(int_qty__lt=5, location_id=1)
    low_quantity_parts_list = [part.serialize() for part in low_quantity_parts]
    low_quantity_parts_json = json.dumps(low_quantity_parts_list)
    return render(request, 'Home.html', {'low_quantity_parts_json': low_quantity_parts_json})



def inventory_changes(request):
    # Get the filter value from the request
    location_filter = request.GET.get('location', '')

    # Apply the filter to the queryset
    if location_filter:
        inventory_changes = InventoryChange.objects.filter(Q(part__location__icontains=location_filter))
    else:
        inventory_changes = InventoryChange.objects.all()

    # Sort and other processing here...

    context = {'inventory_changes': inventory_changes}
    #return render(request, 'inventory_changes.html', context)
    return render(request, '../template/Home.html', context)


def Search(request):
    sort_param = request.GET.get('sort', 'name')  # Default sorting parameter is 'name'
    order_param = request.GET.get('order', 'asc')  # Default order parameter is 'asc'
    client_ip, is_routable = get_client_ip(request)
    
    if sort_param == 'location':
        sort_field = 'location_id'
    elif sort_param == 'barcode':
        sort_field = 'barcode_rm'
    elif sort_param == 'manufacturer':
        sort_field = 'manufacturer_id'
    elif sort_param == 'qty':
        sort_field = 'int_qty'
    else:
        sort_field = sort_param

    if order_param == 'desc':
        sort_field = f'-{sort_field}'

    parts = ItParts.objects.annotate(int_qty=Cast('qty', IntegerField())).order_by(sort_field)
    context = {'parts': parts}

    # Add the low inventory parts data
    low_quantity_parts = ItParts.objects.annotate(int_qty=Cast('qty', IntegerField())).filter(int_qty__lt=5, location_id=1)
    low_quantity_parts_list = [part.serialize() for part in low_quantity_parts]
    low_quantity_parts_json = json.dumps(low_quantity_parts_list)
    context['low_quantity_parts_json'] = low_quantity_parts_json

    # Add the inventory changes data
    inventory_changes = InventoryChange.objects.all()
    context['inventory_changes'] = inventory_changes

    query = request.GET.get('search_res', None)

    if query and request.method == 'GET':
        results = ItParts.objects.filter(barcode_rm=query)
        results1 = ItParts.objects.filter(barcode_add=query)

        for part in results:
            InventoryChange.objects.create(part=part, change_type='remove', change_value=1, source=client_ip)

        for part in results1:
            InventoryChange.objects.create(part=part, change_type='add', change_value=1, source=client_ip)

        ItParts.objects.filter(barcode_rm=query).update(qty=F('qty')-1)
        ItParts.objects.filter(barcode_add=query).update(qty=F('qty')+1)
        context.update({'results': results, 'results1': results1})
    
    # Annotate the InventoryChange QuerySet with the part name from the ItParts model
    #inventory_changes = InventoryChange.objects.annotate(part_name=F('part__name')).all()
    
    #Perform a join between InventoryChange and ItParts using select_related
    inventory_changes = InventoryChange.objects.select_related('part').all()
    context['inventory_changes'] = inventory_changes
    
  '''  # Prepare the data for the context
    inventory_changes_data = [{
        'id': change.id,
        'name': change.part_name,
        'user': change.user,
        'change_type': change.change_type,
        'change_value': change.change_value,
        'timestamp': change.timestamp,
        'source': change.source,
    } for change in inventory_changes]
'''
    # ... remaining code ...

    # Update the context with inventory_changes_data
    context['inventory_changes'] = inventory_changes

    return render(request, '../template/Search.html', context)

def filtered_inventory_changes(request):
    # Get the filter value from the request
    location_filter = request.GET.get('location', '')

    # Apply the filter to the queryset
    if location_filter:
        inventory_changes = InventoryChange.objects.filter(Q(part__location__icontains=location_filter))
    else:
        inventory_changes = InventoryChange.objects.all()

    context = {'inventory_changes': inventory_changes}
    return render(request, 'filtered_inventory_changes.html', context)
  
  
def Home(request):
    # Barcode login functionality
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        try:
            barcode_obj = Barcode.objects.get(barcode=barcode)
            user = barcode_obj.user
            if user is not None:
                login(request, user)
                client_ip, is_routable = get_client_ip(request)
                InventoryChange.objects.create(part=None, change_type='login', change_value=0, source=client_ip, user=request.user)
                return redirect('home')  # Redirect to the home page or any other page after successful login
        except Barcode.DoesNotExist:
            pass
        # If authentication fails, show an error message or handle the failure
        return render(request, '../template/Home.html')  # Render the login template
    # Get the filter value from the request
    location_filter = request.GET.get('location', '')

    # Apply the filter to the queryset
    if location_filter:
        inventory_changes = InventoryChange.objects.filter(Q(part__location__icontains=location_filter))
    else:
        inventory_changes = InventoryChange.objects.all()

    # Sort and other processing here...

    context = {'inventory_changes': inventory_changes}
    
    sort_param = request.GET.get('sort', 'name')  # Default sorting parameter is 'name'
    order_param = request.GET.get('order', 'asc')  # Default order parameter is 'asc'
    client_ip, is_routable = get_client_ip(request)
    
    if sort_param == 'location':
        sort_field = 'location_id'
    elif sort_param == 'barcode':
        sort_field = 'barcode_rm'
    elif sort_param == 'manufacturer':
        sort_field = 'manufacturer_id'
    elif sort_param == 'qty':
        sort_field = 'int_qty'
    else:
        sort_field = sort_param

    if order_param == 'desc':
        sort_field = f'-{sort_field}'

    if location_filter:
        parts = ItParts.objects.filter(location_id=location_filter).annotate(int_qty=Cast('qty', IntegerField())).order_by(sort_field)
    else:
        parts = ItParts.objects.annotate(int_qty=Cast('qty', IntegerField())).order_by(sort_field)

    context = {'parts': parts, 'inventory_changes': inventory_changes, 'location_filter': location_filter}

    # Add the low inventory parts data
    low_quantity_parts = ItParts.objects.annotate(int_qty=Cast('qty', IntegerField())).filter(int_qty__lt=5, location_id="Tolland", Priority=0)
    low_quantity_parts_list = [part.serialize() for part in low_quantity_parts]
    low_quantity_parts_json = json.dumps(low_quantity_parts_list)
    context['low_quantity_parts_json'] = low_quantity_parts_json

    query = request.GET.get('search_res', None)

    if query and request.method == 'GET':
        results = ItParts.objects.filter(barcode_rm=query)
        results1 = ItParts.objects.filter(barcode_add=query)

        for part in results:
            InventoryChange.objects.create(part=part, change_type='remove', change_value=1, source=client_ip)

        for part in results1:
            InventoryChange.objects.create(part=part, change_type='add', change_value=1, source=client_ip)

        ItParts.objects.filter(barcode_rm=query).update(qty=F('qty')-1)
        ItParts.objects.filter(barcode_add=query).update(qty=F('qty')+1)
        context.update({'results': results, 'results1': results1})

    return render(request, '../template/Home.html', context)

def Tolland(request):

    # Page from the theme 
    return render(request, 'pages/Tolland.html')

def EHMS(request):

    # Page from the theme 
    return render(request, 'pages/EHMS.html')

def EHHS(request):

    # Page from the theme 
    return render(request, 'pages/EHHS.html')




'''

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
'''
