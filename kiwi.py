import requests
import click
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup

#python kiwi.py --from Praha --to Brno --date 2017-07-22

@click.command()
@click.option('--from', 'from_')
@click.option('--to', 'to' )
@click.option('--date', 'date', help='2017-12-20')
def url(from_, date, to):
    '''Preparing request.'''
    date_parsed =  datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
    session = requests.Session()
    #    1. request en - sesion ID
    r = session.get('https://www.regiojet.com/en/')
    print(r.status_code)
    print(r.headers['content-type'])

    #2. request aby vratil json destination-en.json
    id_cities_get = session.get('https://www.studentagency.cz/data/wc/ybus-form/destinations-en.json')
    id_cities_json = id_cities_get.json()

    for number in id_cities_json['destinations']:
        for cities in number:
            for cities_number in cities['cities']:
                print(cities_number)
                '''
                if cities_number['cities']['name'] == from_:
                    print(cities_number['cities']['name'])
                    #from_id = cities_number['id']
                '''

    '''
    for number in id_cities_json['destinations']:
        for cities in number:
            for cities_number in cities:
                if cities_number['name'] == to:
                    to_id = cities_number['id']

    print(from_id, to_id)
    '''

    '''
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.find_all('li', class_='toclevel-1')
    #input id="destination_to"
    # soup.select('li.toclevel-1')

    3. request respons body
    '''
    '''
    from_ = 10202002 #Brno
    to = 10202003 #praha
    r = requests.get('https://bustickets.regiojet.com/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false'.format(from_id, to_id, date_parsed, date_parsed))
    print(r.status_code)
    print(r.headers['content-type'])
    #print(r.headers['content-type'])
    '''

'''
[{
  "departure": "2017-12-20 12:45:00",
  "arrival": "2017-12-20 15:00:00",
  "from": "Praha",
  "to": "Ostrava",
  "free_seats": 40,
  "price": 100.0,
  "type": "train", # optional (train/bus)
  "from_id": 47374743, # optional (student agency id)
  "to_id": 26383230 # optional (student agency id)
}]
'''


if __name__ == '__main__':
    url()
