import click

from cli.utils import QuestionaryOption
from functools import wraps
from notifications.notifications import NotificationHandler
from stores.amazon import Amazon
from stores.bestbuy import BestBuyHandler
from stores.evga import Evga
from stores.nvidia import NvidiaBuyer, GPU_DISPLAY_NAMES, CURRENCY_LOCALE_MAP
from utils import selenium_utils

notification_handler = NotificationHandler()


def notify_on_crash(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            pass
        except:
            notification_handler.send_notification(f"nvidia-bot has crashed.")
            raise

    return decorator


@click.group()
def main():
    pass


@click.command()
@click.option(
    "--gpu",
    type=click.Choice(GPU_DISPLAY_NAMES, case_sensitive=False),
    prompt="What GPU are you after?",
    cls=QuestionaryOption,
)
@click.option(
    "--locale",
    type=click.Choice(CURRENCY_LOCALE_MAP.keys(), case_sensitive=False),
    prompt="What locale shall we use?",
    cls=QuestionaryOption,
)
@click.option("--test", is_flag=True)
@click.option("--interval", type=int, default=5)
@notify_on_crash
def nvidia(gpu, locale, test, interval):
    nv = NvidiaBuyer(gpu, locale, test, interval)
    nv.run_items()


@click.command()
@click.option("--no-image", is_flag=True)
@click.option("--headless", is_flag=True)
@click.option("--test", is_flag=True)
@notify_on_crash
def amazon(no_image, headless, test):
    if no_image:
        selenium_utils.no_amazon_image()
    amzn_obj = Amazon(headless=headless)
    amzn_obj.run_item(test=test)


@click.command()
@click.option("--sku", type=str, required=True)
@click.option("--headless", is_flag=True)
@notify_on_crash
def bestbuy(sku, headless):
    bb = BestBuyHandler(sku, headless)
    bb.run_item()


@click.command()
@click.option("--test", is_flag=True)
@click.option("--headless", is_flag=True)
@notify_on_crash
def evga(test, headless):
    ev = Evga(headless)
    ev.buy(test=test)


main.add_command(nvidia)
main.add_command(amazon)
main.add_command(bestbuy)
main.add_command(evga)
