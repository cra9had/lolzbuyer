import dataclasses
import os
from typing import List

from LOLZTEAM import Constants
from LOLZTEAM.API import Market


@dataclasses.dataclass
class TelegramAccount:
    item_id: int
    title: str
    price: int
    seller_id: int
    seller_username: str


class Lolz:
    def __init__(self):
        self.token = os.getenv("LOLZ_TOKEN")
        self.market = Market(token=self.token, language="en")

    def get_telegram_accounts(self) -> List[TelegramAccount]:
        response = self.market.category.telegram.get(pmax=50,
                                          origin=[Constants.Market.ItemOrigin.brute,
                                                  Constants.Market.ItemOrigin.autoreg],
                                          auction="no",
                                          order_by="price_to_up")
        items = response.json()["items"]
        return [TelegramAccount(
            item_id=item.get("item_id"),
            title=item.get("title"),
            price=item.get("rub_price"),
            seller_id=item.get("seller").get("user_id"),
            seller_username=item.get("seller").get("username")
        ) for item in items]
