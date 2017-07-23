import requests
from datetime import datetime, date, time
from pprint import pprint
from bs4 import BeautifulSoup
from redis import StrictRedis
import unidecode
import re
import psycopg2
import psycopg2.extras as pg2


#python kiwi.py --from Brno --to Prague --date 2017-07-22

def search(from_, to, date):
    '''Preparing request and return search data'''
    date_preparsed = datetime.strptime(date, '%Y-%m-%d')
    date_parsed =  date_preparsed.strftime('%Y%m%d')

    db_config = {
        'host': '5.135.242.245',
        'user': 'kiwi',
        'password': 'kiwi',
        'port': 5432,
        'dbname': 'kiwi_weekend'
    }

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM connections_marketa_novackova')
    database_search = cur.fetchall()
    pprint(database_search)
    for item in database_search:
        if item['departure'].date() == date_preparsed.date() and item['src'] == from_ and item['dst'] == to:
            print(item)
            return item


    session = requests.Session()
    r = session.get('https://www.regiojet.com/en/')

    from_id, to_id = get_city_id(to, from_, session)

    #url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0'
    url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    #url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'
    url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    departure = datetime_dep_arr(date, soup, "col_depart gray_gradient")
    arrival = datetime_dep_arr(date, soup, "col_arival gray_gradient")

    free_seats = soup.find('div', class_="col_space gray_gradient").text

    price = soup.find('div', class_="col_price").text


    stdout = [{
        "departure": departure,
        "arrival": arrival,
        "from": from_,
        "to": to,
        "free_seats": int(free_seats),
        "price": int(price[1:4]),
        #"type": "train", # optional (train/bus)
        "from_id": from_id, # optional (student agency id)
        "to_id": to_id # optional (student agency id)
    }]
    pprint(stdout[0])
    database_add(stdout[0], cur, conn)
    return stdout[0]


def database_add(stdout, cur, conn):
    cur.execute(
            """INSERT INTO connections_marketa_novackova (departure, arrival, src, dst, free_seats, price)
               VALUES (%(departure)s, %(arrival)s, %(from_)s, %(to)s, %(free_seats)s, %(price)s);
            """,
            {'departure': stdout['departure'], 'arrival': stdout['arrival'], 'from_': stdout['from'], 'to': stdout['to'], 'free_seats': stdout['free_seats'], 'price': stdout['price']}
        )
    conn.commit()


def datetime_dep_arr(date, soup, dep_arr):
    ''' Make datetime from date and time '''
    date = datetime.strptime(date, '%Y-%m-%d').date()

    time_soup = soup.find('div', class_=dep_arr).text
    time = datetime.strptime(time_soup, '%H:%M').time()
    return datetime.combine(date, time)


def get_city_id_json(id_cities_json, from_or_to):
    ''' Retrun city ID from json '''
    for destination in id_cities_json['destinations']:
        for city in destination['cities']:
            if city['name'] == from_or_to:
                return city['id']


def get_city_id(to, from_, session):
    ''' Return city ID from redis or from json from web '''
    redis_config = {
        'host': '37.139.6.125',
        'password': 'wuaei44INlFurP2qMlng89HmH38',
        'port': 6379
    }
    redis = StrictRedis(**redis_config)
    if redis.get('city_id_{}'.format(slugify(from_))) and redis.get('city_id_{}'.format(slugify(to))):
        from_id = redis.get('city_id_{}'.format(slugify(from_)))
        to_id = redis.get('city_id_{}'.format(slugify(to)))
        print('REDIT USED')
    else:
        id_cities_get = session.get('https://www.studentagency.cz/data/wc/ybus-form/destinations-en.json')
        id_cities_json = id_cities_get.json()
        from_id = get_city_id_json(id_cities_json, from_)
        to_id =  get_city_id_json(id_cities_json, to)
    return from_id.decode('ascii'), to_id.decode('ascii')


def slugify(s):
   '''
   slugify(Brno) -> brno
   slugify(Hradec Králové) -> hradec_kralove
   slugify(Brno hl. nádraží) -> brno_hl_nadrazi
   '''
   s = unidecode.unidecode(s).lower()
   return re.sub(r'\W+', '_', s)
