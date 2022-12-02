from django.shortcuts import render
from . models import ArmorType, Blacksmith, Armor

def index(request):
    armor_count = Armor.objects.count()
    blacksmith_count = Blacksmith.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count+1

    context = {
        'armor_count': armor_count,
        'blacksmith_count': blacksmith_count,
        'armor_type_count': ArmorType.objects.count(),
        'visits_count': visits_count,
    }

    return render(request, 'forge/index.html', context)

def blacksmiths(request):
    return render(
        request, 'forge/blacksmiths.html', 
        {'blacksmiths': Blacksmith.objects.all()})