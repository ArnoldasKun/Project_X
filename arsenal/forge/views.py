from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
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

def blacksmith(request, blacksmith_id):
    return render(
        request, 'forge/blacksmith.html', 
        {'blacksmiths': get_object_or_404(Blacksmith, id=blacksmith_id)}
    )


class ArmorListView(ListView):
    model = Armor
    template_name = 'forge/armor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['armors_count'] = self.get_queryset().count
        return context


class ArmorDetailView(DetailView):
    model = Armor
    template_name = 'forge/armor_detail.html'
        