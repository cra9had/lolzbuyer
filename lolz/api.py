import dataclasses
import os
from typing import List
from LOLZTEAM.Tweaks import SendAsAsync
from LOLZTEAM import Constants
from LOLZTEAM.API import Market
from lolz.converter import TelegramSessionManager


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
        self.session_manager = TelegramSessionManager()

    async def get_telegram_accounts(self) -> List[TelegramAccount]:
        response = await SendAsAsync(self.market.category.telegram.get,
                                     pmax=50,
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
        ) for item in items if item.get("is_reserved") == 0 and item.get("canBuyItem") == True]

    async def buy(self, item: TelegramAccount) -> bool:
        response = await SendAsAsync(self.market.purchasing.fast_buy,
                                     item_id=item.item_id,
                                     price=item.price,
                                     buy_without_validation=False)
        if response.status_code == 200:
            item = response.json().get("item")
            session_info = {
                "accountId": 0,
                "userId": item.get("telegram_id"),
                "dcId": int(item.get("loginData").get("password")),
                "authKey": item.get("login")
            }
            self.session_manager.create_session(session_info, os.path.join(os.getenv("DOWNLOAD_DIR"),
                                                                           f"{item.get('telegram_phone')}.session"))
            return True
        return False

