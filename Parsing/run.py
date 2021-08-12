import os
from tqdm import tqdm
from helper_functions import get_html, get_total_pages, get_ads_urls, write_csv, get_page_data

# Create directory for data sets if doesn't exist
os.makedirs('../Data_sets', exist_ok=True)

# Choice of car type to be parsed
while True:
    brand = input('Enter the car brand (e.g. hyundai, toyota): ')
    model = input('Enter the car model (e.g. sonata, camry): ')
    print('Chosen car -', brand + ' ' + model)
    base_page_url = 'https://www.auto.ru/moskva/cars/' + brand + '/' + model + '/' + 'used/?'
    page_part = 'page='
    rest_part_url = '&output_type=list'
    page_url = base_page_url + page_part + '1' + rest_part_url
    page_html = get_html(page_url)
    if page_html:
        print('Chosen brand and model have been successfully found')
        break
    else:
        print('Parsing error. Apparently, there is a mistake in name of brand and/or car model. Please, try again.',
              'Notice: It\'s only allowed to use lowercase letters.', sep='\n')

# Form data set name
csv_file_name = brand + '_' + model + '.csv'

# Delete old data set with the same name if exists
if csv_file_name in os.listdir('../Data_sets'):
    os.remove('../Data_sets/' + csv_file_name)

# Get total pages with ads
total_pages = get_total_pages(page_html.text)
print('Total number of pages =', total_pages)

# Parsing
for i in tqdm(range(1, total_pages + 1)):
    page_url_gen = base_page_url + page_part + str(i) + rest_part_url
    page_html = get_html(page_url_gen)
    ads_url = get_ads_urls(page_html.text)
    for ad_url in tqdm(ads_url):
        data = get_page_data(ad_url)
        write_csv(csv_file_name, data)

print('Parsing has been successfully finished ')
