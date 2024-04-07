from lolz.api import Lolz
from dotenv import load_dotenv


load_dotenv()


def main():
    lolz = Lolz()
    print(lolz.get_telegram_accounts())


if __name__ == "__main__":
    main()
