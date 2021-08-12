import requests
import csv
import os
from bs4 import BeautifulSoup


def get_html(url):
    """Get html code of the input URL address.

    Parameters
    ----------
    url : str
        URL address.

    Returns
    -------
    html : requests.models.Response
        HTML code of the url.
    """
    html = requests.get(url)
    html.encoding = 'utf-8'

    return html


def get_total_pages(html_text):
    """Get number of total pages with ads for certain car model.

    Parameters
    ----------
    html_text : str
        Text of the HTML code.

    Returns
    -------
    total_pages : int
        Total number of pages.
    """
    soup = BeautifulSoup(html_text, 'lxml')
    upper_class = 'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ' \
                  'ListingPagination-module__page'
    target_class = str(soup.find_all('a', class_=upper_class)[-1].find_all('span', class_='Button__text')[0])
    total_pages = int(target_class.split('>')[1].split('<')[0])

    return total_pages


def get_ads_urls(html_text):
    """Get URLs of ads on the certain page and their number.

    Parameters
    ----------
    html_text : str
        Text of the HTML code.

    Returns
    -------
    ads_urls : list
        URLs list of all ads on the page.
    """
    soup = BeautifulSoup(html_text, 'lxml')
    ads = soup.find_all('a', class_='Link ListingItemTitle__link')

    # Create the list of all ads URLs
    ads_urls = []
    for ad in ads:
        ads_urls.append(ad.get('href'))

    return ads_urls


def write_csv(file_name, data):
    """Write a row of data into the selected CSV file.
    If the file is empty, the labels of columns are written at first.

    Parameters
    ----------
    file_name : str
        The name of selected CSV file.

    data : dict
        Data to be written into the CSV file.
    """
    # Write column's labels
    if file_name not in os.listdir('../Data_sets'):
        with open('../Data_sets/' + file_name, mode='w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['Название', 'Цена, руб.', 'Год выпуска', 'Пробег, км.', 'Тип кузова',
                                 'Цвет', 'Объем двигателя, л.', 'Мощность двигателя, л/с',
                                 'Тип двигателя', 'Налог, руб.', 'Тип коробки передач', 'Привод',
                                 'Положение руля', 'Состояние', 'Число владельцев', 'ПТС',
                                 'Время владения, г.', 'Таможня', 'URL адрес'])

    # Write parsed data
    with open('../Data_sets/' + file_name, mode='a') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow((data['name'], data['price'], data['year'], data['mileage'], data['body_type'],
                             data['color'], data['engine_volume'], data['engine_power'], data['engine_type'],
                             data['tax'], data['transmission'], data['drive_type'], data['wheel'], data['state'],
                             data['owners_number'], data['pts'], data['owning_time'], data['custom'], data['ad_url']))


def get_page_data(ad_url):
    """ Parse data from an ad.

    Parameters
    ----------
    ad_url : str
        URL of an ad to be parsed.

    Returns
    -------
    data : dict
        Data to be written into the CSV file. It contains the following information for a car:
        name, price, year of manufacture, mileage, body type, color, engine volume, engine power,
        engine type, tax, transmission type, drive type, wheel position, state, number of owners,
        PTS type, owning time, custom status, ad url.
    """
    ad_html = get_html(ad_url)
    soup = BeautifulSoup(ad_html.text, 'lxml')
    data = {}

    # Get name
    try:
        data['name'] = soup.find('h1', class_='CardHead__title').text
    except AttributeError:
        data['name'] = ''

    # Get price
    try:
        target_class = soup.find('span', class_='OfferPriceCaption__price').text
        data['price'] = int(''.join(target_class.split('\xa0')[:-1]))
    except (AttributeError, IndexError, KeyError):
        data['price'] = ''

    # Get year
    try:
        data['year'] = int(soup.find('a', class_='Link Link_color_black').text)
    except AttributeError:
        data['year'] = ''

    # Get mileage
    try:
        base_class = soup.find('li', class_='CardInfoRow CardInfoRow_kmAge')
        target_class = base_class.find_all('span', class_='CardInfoRow__cell')[-1]
        data['mileage'] = int(''.join(target_class.text.split('\xa0')[:-1]))
    except (AttributeError, IndexError, KeyError):
        data['mileage'] = ''

    # Get body type
    try:
        data['body_type'] = soup.find('li', class_='CardInfoRow CardInfoRow_bodytype').find('a').text
    except AttributeError:
        data['body_type'] = ''

    # Get color
    try:
        data['color'] = soup.find('li', class_='CardInfoRow CardInfoRow_color').find('a').text
    except AttributeError:
        data['color'] = ''

    # Get engine volume
    try:
        base_class = soup.find('li', class_='CardInfoRow CardInfoRow_engine')
        target_class = base_class.find_all('span', class_='CardInfoRow__cell')[-1]
        data['engine_volume'] = float(target_class.text.split('/')[0].split(' ')[0])
    except (AttributeError, IndexError, KeyError):
        data['engine_volume'] = ''

    # Get engine power
    try:
        base_class = soup.find('li', class_='CardInfoRow CardInfoRow_engine')
        target_class = base_class.find_all('span', class_='CardInfoRow__cell')[-1]
        data['engine_power'] = int(target_class.text.split(' ')[3].split('\xa0')[0])
    except (AttributeError, IndexError, KeyError):
        data['engine_power'] = ''

    # Get engine type
    try:

        data['engine_type'] = soup.find('li', class_='CardInfoRow CardInfoRow_engine').find('a').text
    except AttributeError:
        data['engine_type'] = ''

    # Get tax
    try:
        base_class = soup.find('li', class_='CardInfoRow CardInfoRow_transportTax')
        target_class = base_class.find_all('span', class_='CardInfoRow__cell')[-1]
        data['tax'] = int(''.join(target_class.text.split('\xa0')[:-1]))
    except (AttributeError, IndexError, KeyError):
        data['tax'] = ''

    # Get transmission type
    try:
        data['transmission'] = soup.find('li', class_='CardInfoRow CardInfoRow_transmission').find_all('span')[-1].text
    except (AttributeError, IndexError, KeyError):
        data['transmission'] = ''

    # Get drive type
    try:
        data['drive_type'] = soup.find('li', class_='CardInfoRow CardInfoRow_drive').find_all('span')[-1].text
    except (AttributeError, IndexError, KeyError):
        data['drive_type'] = ''

    # Get wheel position
    try:
        data['wheel'] = soup.find('li', class_='CardInfoRow CardInfoRow_wheel').find_all('span')[-1].text
    except (AttributeError, IndexError, KeyError):
        data['wheel'] = ''

    # Get state
    try:
        data['state'] = soup.find('li', class_='CardInfoRow CardInfoRow_state').find_all('span')[-1].text
    except (AttributeError, IndexError, KeyError):
        data['state'] = ''

    # Get number of owners
    try:
        target_class = soup.find('li', class_='CardInfoRow CardInfoRow_ownersCount').find_all('span')[-1]
        incomplete_owners_number = target_class.text[0]
        if incomplete_owners_number == '3':
            data['owners_number'] = incomplete_owners_number + ' или больше'
        else:
            data['owners_number'] = incomplete_owners_number
    except (AttributeError, IndexError, KeyError):
        data['owners_number'] = ''

    # Get PTS type
    try:
        data['pts'] = soup.find('li', class_='CardInfoRow CardInfoRow_pts').find_all('span')[-1].text
    except (AttributeError, IndexError, KeyError):
        data['pts'] = ''

    # Get owning time
    try:
        target_class = soup.find('li', class_='CardInfoRow CardInfoRow_owningTime').find_all('span')[-1]
        years = int(target_class.text.split(' ')[0])
        months = int(target_class.text.split(' ')[-2])
        data['owning_time'] = round(years + months / 12, 1)
    except (AttributeError, IndexError, KeyError):
        data['owning_time'] = ''

    # Get custom status
    try:
        data['custom'] = soup.find('li', class_='CardInfoRow CardInfoRow_customs').find_all('span')[-1].text
    except (AttributeError, IndexError, KeyError):
        data['custom'] = ''

    # Append ad url
    data['ad_url'] = ad_url

    return data
