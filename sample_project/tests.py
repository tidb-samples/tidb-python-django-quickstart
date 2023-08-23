from django.test import TestCase
from django.urls import reverse_lazy

from sample_project.models import Player


def create_players(number_of_players=10):
    players = []
    for i in range(number_of_players):
        players.append(Player(name=f"Player {i}", coins=100, goods=1))
    Player.objects.bulk_create(players)


class IndexViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-list"))


class PlayerListViewTests(TestCase):
    def test_get_with_no_players(self):
        response = self.client.get(reverse_lazy("player-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no players")
        self.assertQuerysetEqual(response.context["players"], [])

    def test_get_with_players(self):
        create_players(11)
        response = self.client.get(reverse_lazy("player-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["players"]), 11)


class PlayerCreateViewTests(TestCase):
    def test_get(self):
        response = self.client.get(reverse_lazy("player-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a New Player")

    def test_post_success(self):
        response = self.client.post(
            reverse_lazy("player-create"),
            {"name": "Player 1", "coins": 100, "goods": 1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-list"))
        self.assertEqual(Player.objects.count(), 1)

    def test_post_failed_with_empty_name(self):
        response = self.client.post(
            reverse_lazy("player-create"), {"name": "", "coins": 100, "goods": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertEqual(Player.objects.count(), 0)

    def test_post_failed_with_invalid_coins(self):
        response = self.client.post(
            reverse_lazy("player-create"), {"name": "Player 1", "coins": "a", "goods": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a whole number")
        self.assertEqual(Player.objects.count(), 0)


class PlayerBulkCreateViewTests(TestCase):
    def test_post(self):
        response = self.client.post(reverse_lazy("player-bulk-create"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-list"))
        self.assertEqual(Player.objects.count(), 10)


class PlayerDeleteAllViewTests(TestCase):
    def test_post(self):
        create_players(10)
        response = self.client.post(reverse_lazy("player-delete-all"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-list"))
        self.assertEqual(Player.objects.count(), 0)


class PlayerDetailViewTests(TestCase):
    def test_get(self):
        player = Player.objects.create(name="Player 1", coins=100, goods=1)
        response = self.client.get(reverse_lazy("player-detail", args=(player.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Player 1")
        self.assertContains(response, "100")
        self.assertContains(response, "1")
        self.assertEqual(response.context["player"], player)


class PlayerUpdateViewTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(name="Player 1", coins=100, goods=1)

    def test_get(self):
        response = self.client.get(reverse_lazy("player-update", args=(self.player.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Player 1")
        self.assertContains(response, "100")
        self.assertContains(response, "1")
        self.assertEqual(response.context["player"], self.player)

    def test_get_with_non_exists_id(self):
        response = self.client.get(reverse_lazy("player-update", args=(2,)))
        self.assertEqual(response.status_code, 404)

    def test_post_success(self):
        response = self.client.post(
            reverse_lazy("player-update", args=(self.player.id,)),
            {"name": "Player 2", "coins": 200, "goods": 2},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-detail", args=(self.player.id,)))
        self.player.refresh_from_db()
        self.assertEqual(self.player.name, "Player 2")
        self.assertEqual(self.player.coins, 200)
        self.assertEqual(self.player.goods, 2)

    def test_post_failed_with_empty_name(self):
        response = self.client.post(
            reverse_lazy("player-update", args=(self.player.id,)),
            {"name": "", "coins": 200, "goods": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.player.refresh_from_db()
        self.assertEqual(self.player.name, "Player 1")
        self.assertEqual(self.player.coins, 100)
        self.assertEqual(self.player.goods, 1)


class PlayerDeleteViewTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(name="Player 1", coins=100, goods=1)

    def test_get(self):
        response = self.client.get(reverse_lazy("player-delete", args=(self.player.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Player 1")
        self.assertContains(response, "100")
        self.assertContains(response, "1")
        self.assertEqual(response.context["player"], self.player)

    def test_post(self):
        response = self.client.post(reverse_lazy("player-delete", args=(self.player.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-list"))
        self.assertEqual(Player.objects.count(), 0)

    def test_post_with_invalid_id(self):
        response = self.client.post(reverse_lazy("player-delete", args=(self.player.id + 1,)))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Player.objects.count(), 1)


class PlayerTradeViewTests(TestCase):
    NOT_ENOUGH_PLAYERS_TIP = "There are not enough players to start a trade"

    def create_buyer_and_seller(self):
        buyer = Player.objects.create(name="Buyer", coins=100, goods=1)
        seller = Player.objects.create(name="Seller", coins=100, goods=1)
        return buyer, seller

    def test_get_with_no_players(self):
        response = self.client.get(reverse_lazy("player-trade"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.NOT_ENOUGH_PLAYERS_TIP)
        self.assertEqual(response.context["has_enough_players"], False)

    def test_get_with_1_player(self):
        Player.objects.create(name="Player 1", coins=100, goods=100)
        response = self.client.get(reverse_lazy("player-trade"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.NOT_ENOUGH_PLAYERS_TIP)
        self.assertEqual(response.context["has_enough_players"], False)

    def test_get_with_2_players(self):
        self.create_buyer_and_seller()
        response = self.client.get(reverse_lazy("player-trade"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.NOT_ENOUGH_PLAYERS_TIP)
        self.assertEqual(response.context["has_enough_players"], True)

    def test_trade_with_same_player(self):
        buyer, seller = self.create_buyer_and_seller()
        response = self.client.post(
            reverse_lazy("player-trade"),
            {
                "buyer": buyer.id,
                "seller": buyer.id,
                "goods": 1,
                "coins": 100,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Buyer and seller cannot be the same person.")
        buyer.refresh_from_db()
        seller.refresh_from_db()
        self.assertEqual(buyer.coins, 100)
        self.assertEqual(buyer.goods, 1)
        self.assertEqual(seller.coins, 100)
        self.assertEqual(seller.goods, 1)

    def test_trade_with_players_buyer_not_enough_coins(self):
        buyer, seller = self.create_buyer_and_seller()
        buyer.coins = 0
        buyer.save()
        response = self.client.post(
            reverse_lazy("player-trade"),
            {
                "buyer": buyer.id,
                "seller": seller.id,
                "goods": 1,
                "coins": 100,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Buyer does not have enough coins.")
        buyer.refresh_from_db()
        seller.refresh_from_db()
        self.assertEqual(buyer.coins, 0)
        self.assertEqual(buyer.goods, 1)
        self.assertEqual(seller.coins, 100)
        self.assertEqual(seller.goods, 1)

    def test_trade_with_players_seller_not_enough_goods(self):
        buyer, seller = self.create_buyer_and_seller()
        seller.goods = 0
        seller.save()
        response = self.client.post(
            reverse_lazy("player-trade"),
            {
                "buyer": buyer.id,
                "seller": seller.id,
                "goods": 1,
                "coins": 100,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seller does not have enough goods.")
        buyer.refresh_from_db()
        seller.refresh_from_db()
        self.assertEqual(buyer.coins, 100)
        self.assertEqual(buyer.goods, 1)
        self.assertEqual(seller.coins, 100)
        self.assertEqual(seller.goods, 0)

    def test_trade_with_players_success(self):
        buyer, seller = self.create_buyer_and_seller()
        response = self.client.post(
            reverse_lazy("player-trade"),
            {
                "buyer": buyer.id,
                "seller": seller.id,
                "goods": 1,
                "coins": 100,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy("player-list"))
        buyer.refresh_from_db()
        seller.refresh_from_db()
        self.assertEqual(buyer.coins, 0)
        self.assertEqual(buyer.goods, 2)
        self.assertEqual(seller.coins, 200)
        self.assertEqual(seller.goods, 0)
