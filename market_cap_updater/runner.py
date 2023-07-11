from main import update_csv, update_text
from hard_parse import read
from time import time
from requests import get

from os import environ
environ["GITHUB_TOKEN"] = ''
environ["GITHUB_USERNAME"] = ''


def print_error(text):
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n{text}\n'
          f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


def print_msg(text):
    print(f'***************************************************************\n{text}\n'
          f'***************************************************************')


def get_with_timestamp(url):
    return url + "?timestamp=" + str(time())


def txt_handle():
    print_msg('Starting Java Program')
    update_text()
    print_msg('Done Running Java Program....\n Ending csv_handle()')

    return True


def csv_handle():
    link_t = 'https://raw.githubusercontent.com/carter4299/custom-PPO-Notebook/main/market_cap_updater/stockanalysis.txt'
    true_total = 5856

    with open('log.txt', 'w') as g:
        response_txt = get(get_with_timestamp(link_t))
        g.write(f'Reading initial txt\n{str(response_txt)}\n')
        data_t = response_txt.text
        if data_t is None:
            print_error('Error loading in updated tick_info.csv')
            return False

        print_msg('Loaded updated txt....\n Starting parser')
        data_c_i = read(data_t)

        print_msg('CSV formatted....\n Testing csv format validity')
        if data_c_i is None:
            print_error('Error loading in initial data tick_info.csv')
            return False
        our_total = data_c_i.shape[0]
        scraped = round(our_total / true_total, 2) * 100
        print_msg(f'Scraped {scraped}% of data from https://stockanalysis.com/stocks/')
        if scraped < 90:
            print_error('Error(Low Count) while scraping data from https://stockanalysis.com/stocks/')
            return False
        for _ in data_c_i['s']:
            if len(str(_)) > 6 or len(str(_)) == 0:
                print_error('Error(Ticker Length) while scraping data from https://stockanalysis.com/stocks/')
                return False

        print_msg(f'CSV formatted correctly....\n Uploading to Github')
        response = update_csv(data_c_i)
        g.write(f'CSV update status\n{str(response)}\n')

        print_msg(f'Upload finished....\n Ending csv_handle()')
        g.close()

    return True


def run():
    if txt_handle():
        print_msg('Text Changed....\n Attempting to update tick_info.csv')
        if csv_handle():
            print_msg('CSV Changed....\n Closing :) ')
        else:
            print('Unexpected Error. Check csv_logger')
    else:
        print('Unexpected Error. Check text_logger')


if __name__ == '__main__':
    run()
