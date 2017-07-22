
import click
from search import search

@click.command()
@click.option('--from', 'from_')
@click.option('--to', 'to' )
@click.option('--date', 'date', help='2017-12-20')
def cli(from_, to, date):
    return search(from_, to, date)


if __name__ == '__main__':
    cli()
