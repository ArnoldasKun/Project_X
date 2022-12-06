from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from . models import ArmorType, Blacksmith, Armor, ArmorOrder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from . forms import ArmorReviewForm

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
    paginator = Paginator(Blacksmith.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_blacksmiths = paginator.get_page(page_number)
    return render(
        request, 'forge/blacksmiths.html', 
        {'blacksmiths': paged_blacksmiths})

def blacksmith(request, blacksmith_id):
    return render(
        request, 'forge/blacksmith.html', 
        {'blacksmith': get_object_or_404(Blacksmith, id=blacksmith_id)}
    )


class ArmorListView(ListView):
    model = Armor
    paginate_by = 5
    template_name = 'forge/armor_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(summary__icontains=search))
        armor_type_id = self.request.GET.get('armor_type_id')
        if armor_type_id:
            queryset = queryset.filter(armor_type__id=armor_type_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['armors_count'] = self.get_queryset().count()
        armor_type_id = self.request.GET.get('armor_type_id')
        context['armor_types'] = ArmorType.objects.all()
        if armor_type_id:
            context['armor_type'] = get_object_or_404(ArmorType, id=armor_type_id)
        return context


class ArmorDetailView(FormMixin, DetailView):
    model = Armor
    template_name = 'forge/armor_detail.html'
    form_class = ArmorReviewForm

    def get_success_url(self):
        return reverse('armor', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(self.request, "You're posting too much!")
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.armor = self.get_object()
        form.instance.buyer = self.request.user
        form.save()
        messages.success(self.request, 'Your review has been posted!')
        return super().form_valid(form)

    def get_initial(self):
        return {
            'armor': self.get_object(),
            'buyer': self.request.user,
        }


class UserArmorListView(LoginRequiredMixin, ListView):
    model = ArmorOrder
    template_name = 'forge/user_armor_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(buyer=self.request.user).order_by('due_back')
        return queryset
        