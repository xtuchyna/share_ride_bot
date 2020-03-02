import facebook
from FacebookWebBot import FacebookBot
from datetime import datetime
import click
import os

SHARE_RIDE_GROUP_ID = '115470321831897'
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN')

USERNAME = os.getenv('FB_U')
PASSWORD = os.getenv('FB_P')


@click.command()
@click.option(
    '--time',
    '-t',
)
@click.option(
    '--day',
    '-d',
)
@click.option(
    '--to-city',
    '-c',
    'city',
)
@click.option(
    '--people',
    '-p',
)
@click.option(
    '--api',
    '-a',
    default=False
)
def main(time, day, city, api, people):
    message = generate_message(to_city=city, day=day, time=time, people_num=people)
    if api:
        post_offer_api(message)
    else:
        post_offer_selenium(message)


def get_sk_day(day: str):
    if day == 'mo':
        return 'pondelok'
    elif day == 'tu':
        return 'utorok'
    elif day == 'we':
        return 'stred'
    elif day == 'th':
        return 'stvrtok'
    elif day == 'fr':
        return 'piatok'
    elif day == 'sa':
        return 'sobota'
    elif day == 'su':
        return 'nedela'


def generate_message(to_city: str, day: str, time: str, people_num: int) -> str:
    
    _to_city = 'TN' if to_city == 'T' else 'Brno'
    _from_city = 'TN' if to_city == 'B' else 'Brno'

    message = [f'PONUKAM {people_num} miesta',
               f'{_from_city} -> {_to_city}',
               f'{get_sk_day(day)} o {time}',
               '4 v aute, 6e']

    return '\n'.join(message)


def post_offer_selenium(message: str):
    bot = FacebookBot()
    bot.set_page_load_timeout(10)
    bot.login(email=USERNAME, password=PASSWORD)
    bot.postInGroup(groupURL='https://www.facebook.com/groups/115470321831897/', text=message)

def post_offer_api(message: str) -> None:
    print('connecting...')
    graph = facebook.GraphAPI(access_token=FACEBOOK_TOKEN)
    print('connected')

    print(f'The posted message will be:\n{message}')
    print('writing post...')
    graph.put_object(parent_object='me',
                    connection_name='feed',
                    message=message)
    print('successfully posted')


if __name__ == "__main__":
    main()