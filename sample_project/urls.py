"""
URL configuration for sample_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from sample_project import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("players/", views.PlayerListView.as_view(), name="player-list"),
    path("players/create/", views.PlayerCreateView.as_view(), name="player-create"),
    path("players/bulk-create/", views.PlayerBulkCreateView.as_view(), name="player-bulk-create"),
    path("players/delete-all/", views.PlayerDeleteAllView.as_view(), name="player-delete-all"),
    path("players/<int:pk>/", views.PlayerDetailView.as_view(), name="player-detail"),
    path("players/<int:pk>/update/", views.PlayerUpdateView.as_view(), name="player-update"),
    path("players/<int:pk>/delete/", views.PlayerDeleteView.as_view(), name="player-delete"),
    path("players/trade/", views.PlayerTradeView.as_view(), name="player-trade"),
]
