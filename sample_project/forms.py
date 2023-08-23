from django import forms
from django.db import models, transaction

from sample_project.models import Player


class TradeForm(forms.Form):
    buyer = forms.ModelChoiceField(label="Buyer", queryset=Player.objects.all(), required=True)
    seller = forms.ModelChoiceField(label="Seller", queryset=Player.objects.all(), required=True)
    goods = forms.IntegerField(label="Buy goods", required=True)
    coins = forms.IntegerField(label="Need coins", required=True)

    def clean(self):
        cleaned_data = super().clean()
        buyer = cleaned_data.get("buyer")
        seller = cleaned_data.get("seller")
        goods = cleaned_data.get("goods")
        coins = cleaned_data.get("coins")

        if buyer == seller:
            raise forms.ValidationError("Buyer and seller cannot be the same person.")

        if buyer.coins < coins:
            raise forms.ValidationError("Buyer does not have enough coins.")

        if seller.goods < goods:
            raise forms.ValidationError("Seller does not have enough goods.")
        return cleaned_data

    @transaction.atomic
    def save(self):
        buyer = self.cleaned_data.get("buyer")
        seller = self.cleaned_data.get("seller")
        goods = self.cleaned_data.get("goods")
        coins = self.cleaned_data.get("coins")

        seller = Player.objects.select_for_update().get(id=seller.id)
        if seller.goods < goods:
            raise forms.ValidationError("Seller does not have enough goods.")

        buyer = Player.objects.select_for_update().get(id=buyer.id)
        if buyer.coins < coins:
            raise forms.ValidationError("Buyer does not have enough coins.")

        seller.goods = models.F("goods") - goods
        seller.coins = models.F("coins") + coins
        seller.save()
        buyer.goods = models.F("goods") + goods
        buyer.coins = models.F("coins") - coins
        buyer.save()
