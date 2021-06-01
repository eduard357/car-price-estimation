from functions import get_html, get_total_pages, get_ads_url, write_csv, get_page_data

# Create dictionary
columns_name = {'name': 'Название',
                'price': 'Цена, руб.',
                'year': 'Год выпуска',
                'mileage': 'Пробег, км.',
                'body_type': 'Кузов',
                'color': 'Цвет',
                'engine_volume': 'Объем двигателя, л.',
                'engine_power': 'Мощность двигателя, л/с',
                'engine_type': 'Двигатель',
                'tax': 'Налог, руб.',
                'transmission': 'Коробка передач',
                'drive': 'Привод',
                'wheel': 'Руль',
                'state': 'Состояние',
                'owners_counter': 'Число владельцев',
                'pts': 'ПТС',
                'custom': 'Таможня',
                'ad_url': 'URL адрес'}

# Input data processing
while True:
    mark = input('Введите модель машины: ')
    model = input('Введите марку машины: ')
    print('Выбранная модель -', mark + ' ' + model)
    base_page_url = 'https://www.auto.ru/moskva/cars/' + mark + '/' + model + '/' + 'used/?'
    page_part = 'page='
    rest_part_url = '&output_type=list'
    page_url = base_page_url + page_part + '1' + rest_part_url
    page_html = get_html(page_url)
    if str(page_html) != '<Response [404]>':
        print('Выбранные модель и марка успешно найдены')
        break
    else:
        print('Ошибка парсинга страницы. Вероятно, допущена ошибка в названии модели и/или марки автомобиля. Попробуйте еще раз')

csv_file_name = mark + '_' + model + '.csv'
write_csv(csv_file_name, columns_name)
total_pages = get_total_pages(page_html.text)
print('Всего страниц найдено =', total_pages)

# Parsing
for i in range(1, total_pages + 1):
    page_url_gen = base_page_url + page_part + str(i) + rest_part_url
    print('Текущая страница =', i, 'из', total_pages)
    print('URL = ', page_url_gen)
    page_html = get_html(page_url_gen)
    ads_url, ads_number_on_page = get_ads_url(page_html.text)
    j = 0
    for elem in ads_url:
        ad_html = get_html(elem)
        data = get_page_data(ad_html.text, elem)
        write_csv(csv_file_name, data)
        j += 1
        if j == 1:
            print('Информация считана с', j, 'объявления из', ads_number_on_page, 'на странице', i)
        else:
            print('Информация считана с', j, 'объявлений из', ads_number_on_page, 'на странице', i)
print('Парсинг успешно завершен ')
