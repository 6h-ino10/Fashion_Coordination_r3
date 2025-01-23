from django import forms
from .models import Coordination,Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'season', 'image', 'memo']

class CoordinationForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Coordination
        fields = ['category','season','items','coordination_image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['items'].queryset = Item.objects.filter(user=user)
        else:
            self.fields['items'].queryset = Item.objects.none()


