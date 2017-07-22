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
    print(r.status_code)
    print(r.headers['content-type'])

    id_cities_get = session.get('https://www.studentagency.cz/data/wc/ybus-form/destinations-en.json')
    id_cities_json = id_cities_get.json()

    for destination in id_cities_json['destinations']:
        for city in destination['cities']:
            if city['name'] == from_:
                print(city['id'], city['name'])
                from_id = city['id']

    for destination in id_cities_json['destinations']:
        for city in destination['cities']:
            if city['name'] == to:
                print(city['id'], city['name'])
                to_id = city['id']

    url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0'
    #url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'
    #url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    print(r.status_code)
    print(r.headers['content-type'])
    print(url)
    #print(r.headers['content-type'])

    #print(r.text)
    date_departure = datetime.strptime(date, '%Y-%m-%d').date()

    soup = BeautifulSoup(r.text, 'html.parser')

    time_departure_soup = soup.find('div', class_="col_depart gray_gradient").text
    print(time_departure_soup)
    time_departure = datetime.strptime(time_departure_soup, '%H:%M').time()
    departure = datetime.combine(date_departure, time_departure)

    time_arrival_soup = soup.find('div', class_="col_arival gray_gradient").text
    print(time_arrival_soup)
    time_arrival = datetime.strptime(time_departure_soup, '%H:%M').time()
    arrival = datetime.combine(date_departure, time_arrival)

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


if __name__ == '__main__':
    url()
