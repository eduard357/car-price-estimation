import os
from functions import get_html, get_total_pages, get_ads_url, write_csv, get_page_data

# Create dictionary
columns_name = ['name', 'price', 'year', 'mileage', 'body_type', 'color',
                'engine_volume', 'engine_power', 'engine_type', 'tax',
                'transmission', 'drive', 'wheel', 'state',
                'owners_counter', 'pts', 'custom', 'ad_url']

# Input data processing
while True:
    mark = input('Enter the car model: ')
    model = input('Enter the car brand: ')
    print('Chosen model -', mark + ' ' + model)
    base_page_url = 'https://www.auto.ru/moskva/cars/' + mark + '/' + model + '/' + 'used/?'
    page_part = 'page='
    rest_part_url = '&output_type=list'
    page_url = base_page_url + page_part + '1' + rest_part_url
    page_html = get_html(page_url)
    if str(page_html) != '<Response [404]>':
        print('Chosen model and brand have been successfully found')
        break
    else:
        print('Error of page parsing. Apparently, it\'s made a mistake in name of model and/or car brand. Try again')

csv_file_name = mark + '_' + model + '.csv'
if ('../Data_sets/' + csv_file_name) in os.listdir('../Data_sets/'):
    os.remove('../Data_sets/' + csv_file_name)

write_csv(csv_file_name, columns_name)
total_pages = get_total_pages(page_html.text)
print('Total number of pages =', total_pages)

# Parsing
for i in range(1, total_pages + 1):
    page_url_gen = base_page_url + page_part + str(i) + rest_part_url
    print('Current page =', i, 'from', total_pages)
    print('URL = ', page_url_gen)
    page_html = get_html(page_url_gen)
    ads_url, ads_number_on_page = get_ads_url(page_html.text)
    j = 0
    for elem in ads_url:
        ad_html = get_html(elem)
        data = get_page_data(ad_html.text, elem)
        write_csv(csv_file_name, data.values())
        j += 1
        print('Information read from', j, 'ad from', ads_number_on_page, 'on the page', i)
print('Parsing has been successfully finished ')
