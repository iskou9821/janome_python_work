# coding:UTF-8

from Janome.Rakuen import RakutenService

rakuten = RakutenService('./config.ini')

location_dict = rakuten.get_location_directory()

print(location_dict)

hotels = rakuten.get_hotels(location_dict['北海道'])

print(hotels)