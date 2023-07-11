import sys
import pandas as pd


def print_error(text):
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n{text}\n'
          f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


def print_msg(text):
    print(f'***************************************************************\n{text}\n'
          f'***************************************************************')


def parse(d):
    entries = d.split('},{')
    replace = [['{', ''], ['}', ''], [', Inc', ' Inc'], [', Ltd', ' Ltd'], [', Plc', 'Plc'], [', inc.', ' inc.'],
               [', Fixtures & Appliances', ' Fixtures & Appliances'], [', SAB de CV', ' SAB de CV'], [', L.P.', ' L.P.'],
               [', S. A.', ' S. A.'], [', S.A.', ' S.A.'], [', Dickinson and Company', ' Dickinson and Company'],
               [', Co.', ' Co.'], [', LLC', ' LLC'], [', Corp.', ' Corp.'], [', Limited', ' Limited'],
               [', Ruger & Company Inc.', ' Ruger & Company Inc.']]
    result = []
    error = []
    for entry in entries:
        for rep in replace:
            entry = entry.replace(rep[0], rep[1])
        fields = entry.split(',')
        stock = {}
        for field in fields:
            try:
                key, value = field.split(':')
                stock[key] = value.strip('"')
            except ValueError:
                error.append(field)
                continue

        result.append(stock)
    print_msg(f'Added {len(result)} datapoints....\n Returning to read()')
    print_error(f'Error Could not parse {error}')
    return result


def read(data):
    if data is None:
        print_error(f'Big F')
        sys.exit()
    print_msg('Data Received... \nParser Started')
    stocks = parse(data)
    if stocks is None:
        print_error(f'Big F')
        sys.exit()
    print_msg('Parser Ended... \nReturning to update_csv()')
    return pd.DataFrame(stocks)



