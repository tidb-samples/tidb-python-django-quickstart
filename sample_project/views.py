import logging

from django import forms
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
)

from sample_project.forms import TradeForm
from sample_project.models import Player

logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("player-list"))


class PlayerListView(ListView):
    model = Player
    template_name = "list.html"
    context_object_name = "players"


class PlayerCreateView(CreateView):
    model = Player
    template_name = "create.html"
    fields = ["name", "coins", "goods"]
    success_url = reverse_lazy("player-list")


class PlayerBulkCreateView(View):
    def post(self, request, *args, **kwargs):
        players = []
        for i in range(10):
            players.append(Player(name=f"Player {i}", coins=100, goods=1))
        Player.objects.bulk_create(players)
        return HttpResponseRedirect(reverse_lazy("player-list"))


class PlayerDeleteAllView(View):
    def post(self, request, *args, **kwargs):
        Player.objects.all().delete()
        return HttpResponseRedirect(reverse_lazy("player-list"))


class PlayerDetailView(DetailView):
    model = Player
    template_name = "detail.html"
    context_object_name = "player"


class PlayerUpdateView(UpdateView):
    model = Player
    template_name = "update.html"
    fields = ["name", "coins", "goods"]

    def get_success_url(self):
        return reverse_lazy("player-detail", kwargs={"pk": self.object.pk})


class PlayerDeleteView(DeleteView):
    model = Player
    template_name = "delete.html"
    success_url = reverse_lazy("player-list")


class PlayerTradeView(FormView):
    template_name = "transaction.html"
    form_class = TradeForm
    initial = {"goods": 1, "coins": 10}
    success_url = reverse_lazy("player-list")

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        try:
            form.save()
        except forms.ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        except Exception:
            import traceback

            logger.error(traceback.format_exc())
            form.add_error(None, "Unknown error occurred.")
            return self.form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_enough_players"] = Player.objects.count() >= 2
        return context
