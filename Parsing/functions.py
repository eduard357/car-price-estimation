import requests
from bs4 import BeautifulSoup
import csv
import os


# Get html code of the input URL address
def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r


# Get total pages number
def get_total_pages(page_html_text):
    soup = BeautifulSoup(page_html_text, 'lxml')
    upper_class = 'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page'
    total_pages = \
        str(soup.find_all('a', class_=upper_class)[-1].find_all('span', class_='Button__text')[0]).split('>')[1].split(
            '<')[
            0]
    return int(total_pages)


# Get URLs list of ads only for used cars
def get_ads_url(page_html_text):
    soup = BeautifulSoup(page_html_text, 'lxml')
    ads = soup.find_all('a', class_='Link ListingItemTitle-module__link')

    # Create the list of all ads URLs
    ads_url = []
    for i in range(len(ads)):
        ads_url.append(ads[i].get('href'))

    # Delete the ad if the car isn't used
    for elem in ads_url:
        if elem.find('used') == -1:
            ads_url.remove(elem)

    ads_number_on_page = len(ads_url)
    return ads_url, ads_number_on_page


# Write a row of data into the selected CSV file
def write_csv(file_, data):
    os.makedirs("../Data_sets", exist_ok=True)
    with open('../Data_sets/' + file_, 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['price'], data['year'], data['mileage'], data['body_type'], data['color'],
                         data['engine_volume'], data['engine_power'], data['engine_type'], data['tax'],
                         data['transmission'], data['wheel'], data['state'], data['owners_counter'], data['pts'],
                         data['custom'], data['ad_url']))


# Get data from a page
def get_page_data(page_html_text, ad_url):
    soup = BeautifulSoup(page_html_text, 'lxml')

    def convert(list_):
        result = ''
        for elem in list_:
            try:
                int(elem)
            except:
                break
            else:
                result += elem
        return result

    try:
        name = str(soup.find('div', class_='CardSidebarActions__title')).split('>')[1].split('<')[0]
    except:
        name = ''

    try:
        price_incomplete = str(soup.find('span', class_='OfferPriceCaption__price')).split('>')[1].split('\xa0')
    except:
        price = ''
    else:
        price = int(convert(price_incomplete))

    try:
        year = int(str(soup.find('a', class_='Link Link_color_black')).split('>')[1].split('<')[0])
    except:
        year = ''

    try:
        mileage_incomplete = str(
            soup.find('li', class_='CardInfoRow CardInfoRow_kmAge').find_all('span', class_='CardInfoRow__cell')[
                -1]).split('>')[1].split('\xa0')
    except:
        mileage = ''
    else:
        mileage = int(convert(mileage_incomplete))

    try:
        body_type = soup.find('li', class_='CardInfoRow CardInfoRow_bodytype').find('a').text
    except:
        body_type = ''

    try:
        color = soup.find('li', class_='CardInfoRow CardInfoRow_color').find('a').text
    except:
        color = ''

    try:
        engine_volume = round(float((str(
            soup.find('li', class_='CardInfoRow CardInfoRow_engine').find_all('span', class_='CardInfoRow__cell')[
                -1]).split('>')[2].split(' ')[0])), 1)
    except:
        engine_volume = ''

    try:
        engine_power = int(str(
            soup.find('li', class_='CardInfoRow CardInfoRow_engine').find_all('span', class_='CardInfoRow__cell')[
                -1]).split('/ ')[1].split('\xa0')[0])
    except:
        engine_power = ''

    try:
        engine_type = soup.find('li', class_='CardInfoRow CardInfoRow_engine').find('a').text
    except:
        engine_type = ''

    try:
        tax_incomplete = str(
            soup.find('li', class_='CardInfoRow CardInfoRow_transportTax').find_all('span', class_='CardInfoRow__cell')[
                -1]).split('>')[1].split('\xa0')
    except:
        tax = ''
    else:
        tax = convert(tax_incomplete)

    try:
        transmission = soup.find('li', class_='CardInfoRow CardInfoRow_transmission').find_all('span')[-1].text
    except:
        transmission = ''

    try:
        drive = soup.find('li', class_='CardInfoRow CardInfoRow_drive').find_all('span')[-1].text
    except:
        drive = ''

    try:
        wheel = soup.find('li', class_='CardInfoRow CardInfoRow_wheel').find_all('span')[-1].text
    except:
        wheel = ''

    try:
        state = soup.find('li', class_='CardInfoRow CardInfoRow_state').find_all('span')[-1].text
    except:
        state = ''

    try:
        owners_counter_incomplete = soup.find('li', class_='CardInfoRow CardInfoRow_ownersCount').find_all('span')[
            -1].text.split('\xa0')
    except:
        owners_counter = ''
    else:
        owners_counter = ' '.join(owners_counter_incomplete)

    try:
        pts = soup.find('li', class_='CardInfoRow CardInfoRow_pts').find_all('span')[-1].text
    except:
        pts = ''

    try:
        custom = soup.find('li', class_='CardInfoRow CardInfoRow_customs').find_all('span')[-1].text
    except:
        custom = ''

    data = {'name': name,
            'price': price,
            'year': year,
            'mileage': mileage,
            'body_type': body_type,
            'color': color,
            'engine_volume': engine_volume,
            'engine_power': engine_power,
            'engine_type': engine_type,
            'tax': tax,
            'transmission': transmission,
            'drive': drive,
            'wheel': wheel,
            'state': state,
            'owners_counter': owners_counter,
            'pts': pts,
            'custom': custom,
            'ad_url': ad_url}

    return data
