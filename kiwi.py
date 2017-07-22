import requests
import click
from datetime import datetime, date, time
from pprint import pprint
from bs4 import BeautifulSoup

#python kiwi.py --from Brno --to Prague --date 2017-07-22

@click.command()
@click.option('--from', 'from_')
@click.option('--to', 'to' )
@click.option('--date', 'date', help='2017-12-20')
def url(from_, date, to):
    '''Preparing request.'''
    date_parsed =  datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
    session = requests.Session()
    r = session.get('https://www.regiojet.com/en/')

    id_cities_get = session.get('https://www.studentagency.cz/data/wc/ybus-form/destinations-en.json')
    id_cities_json = id_cities_get.json()

    from_id = get_city_id(id_cities_json, from_)
    to_id =  get_city_id(id_cities_json, to)

    url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0'
    #url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'
    #url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    departure = datetime_dep_arr(date, soup, "col_depart gray_gradient")
    arrival = datetime_dep_arr(date, soup, "col_arival gray_gradient")

    free_seats = soup.find('div', class_="col_space gray_gradient").text

    price = soup.find('div', class_="col_price").text

    #import pdb; pdb.set_trace()
    stdout = [{
        "departure": departure,
        "arrival": arrival,
        "from": from_,
        "to": to,
        "free_seats": int(free_seats),
        "price": int(price[:4]),
        #"type": "train", # optional (train/bus)
        "from_id": from_id, # optional (student agency id)
        "to_id": to_id # optional (student agency id)
    }]
    pprint(stdout)


def get_city_id(id_cities_json, from_or_to):
    for destination in id_cities_json['destinations']:
        for city in destination['cities']:
            if city['name'] == from_or_to:
                #print(city['id'], city['name'])
                return city['id']


def datetime_dep_arr(date, soup, dep_arr):
    date = datetime.strptime(date, '%Y-%m-%d').date()

    time_soup = soup.find('div', class_=dep_arr).text
    #print(time_soup)
    time = datetime.strptime(time_soup, '%H:%M').time()
    return datetime.combine(date, time)



if __name__ == '__main__':
    url()
