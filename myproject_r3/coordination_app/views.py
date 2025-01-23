from django.shortcuts import render
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item,Coordination 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import CoordinationForm, ItemForm
from users.views import get_weather_for_user

class ItemListView(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'coordination_app/item_list.html'
    context_object_name = 'item_list'
    paginate_by = 5

    def get_queryset(self):
        print("Logged in User ID:", self.request.user.id)

        queryset = Item.objects.filter(user=self.request.user)
        print("Filtered Items:", queryset)
        
        category_id = self.request.GET.get('category')
        season = self.request.GET.get('season')

        if category_id:
            queryset = queryset.filter(category=category_id)

        if season:
            queryset = queryset.filter(season=season)

        print("Diltered Items after category/season:", queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['weather_data'] = get_weather_for_user(self.request.user)

        return context
    
class ItemCreateView(LoginRequiredMixin,CreateView):
    model = Item
    #fields = '__all__'
    form_class = ItemForm
    template_name = 'coordination_app/item_form.html'
    success_url = reverse_lazy('item_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin,UpdateView):
    model = Item
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('item_list')

class ItemDeleteView(LoginRequiredMixin,DeleteView):
    model = Item
    success_url = reverse_lazy('item_list')

class CoordinationListView(LoginRequiredMixin,ListView):
    model = Coordination
    template_name = 'coordination_app/coordination_list.html'
    context_object_name = 'coordination_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        
        category_id = self.request.GET.get('category')
        season = self.request.GET.get('season')
        item = self.request.GET.get('item')

        if category_id:
            queryset = queryset.filter(category=category_id)

        if season:
            queryset = queryset.filter(season=season)

        if item:
            queryset = queryset.filter(items=item)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coordination_items'] = Item.objects.filter(user=self.request.user)
        context['weather_data'] = get_weather_for_user(self.request.user)

        return context


def coordination_list(request):
    coordination_list = Coordination.objects.all()
    return render(request,'coordination_app/coordination_list.html',{'coordination_list':coordination_list})

class CoordinationCreateView(LoginRequiredMixin,CreateView):
    model = Coordination
    form_class = CoordinationForm
    template_name = 'coordination_app/coordination_form.html'
    success_url = reverse_lazy('coordination_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CoordinationUpdateView(LoginRequiredMixin,UpdateView):
    model = Coordination
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('coordination_list')

class CoordinationDeleteView(LoginRequiredMixin,DeleteView):
    model = Coordination
    success_url = reverse_lazy('coordination_list')

