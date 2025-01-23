from django.urls import path
from coordination_app import views

urlpatterns =[
    path('items/',views.ItemListView.as_view(),name='item_list'), 
    path('coordination/',views.CoordinationListView.as_view(),name='coordination_list'),
    path('items/new',views.ItemCreateView.as_view(),name='item_new'), 
    path('items/<int:pk>/edit/',views.ItemUpdateView.as_view(),name='item_edit'),
    path('items/<int:pk>/delete/',views.ItemDeleteView.as_view(),name='item_delete'), 
    path('coordination/new/',views.CoordinationCreateView.as_view(),name='coordination_new'),
    path('coordination/<int:pk>/edit/',views.CoordinationUpdateView.as_view(),name='coordination_edit'), 
    path('coordination/<int:pk>/delete/',views.CoordinationDeleteView.as_view(),name='coordination_delete'),
]
