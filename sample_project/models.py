from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    coins = models.IntegerField(default=100)
    goods = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sample_project_players"
        verbose_name = "player"
        verbose_name_plural = "players"

    def __str__(self):
        return f"{self.name}(id: {self.id}, coins: {self.coins}, goods: {self.goods})"
