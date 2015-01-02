__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150102'
__version__ = '0.00'

import csv


def csv_writer(data, file_name):

    fout = open(file_name, mode='wb')
    import pprint
    pprint.pprint(data)
    writer = csv.DictWriter(fout, data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    fout.flush()
    fout.close()

    return True