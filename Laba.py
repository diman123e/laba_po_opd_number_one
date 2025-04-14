import requests
from bs4 import BeautifulSoup

# URL страницы с объявлениями
url = 'https://auto.drom.ru/region55/new/all/'

# Заголовки для имитации запроса от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Отправляем GET-запрос на сайт
print("Отправка запроса на сайт...")
response = requests.get(url, headers=headers)

# Проверяем, что запрос успешен
if response.status_code == 200:
    print("Запрос успешен. Парсим данные...")
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы с объявлениями
    ads = soup.find_all('div', attrs={
        'data-ftid': 'bulls-list_bull',
        'class': 'css-1f68fiz ea1vuk60'
    }, limit=20)

    if not ads:
        print("Объявления не найдены. Проверьте структуру HTML.")
    else:
        print(f"Найдено объявлений: {len(ads)}")
        # Открываем файл для записи результатов
        with open('car_ads.txt', 'w', encoding='utf-8') as file:
            # Проходим по каждому объявлению
            for ad in ads:
                try:
                    # Извлекаем заголовок объявления
                    title = ad.find('h3', class_='css-16kqa8y efwtv890').text.strip()
                except AttributeError:
                    title = "Нет заголовка"

                try:
                    # Извлекаем цену
                    price = ad.find('span', class_='css-46itwz e162wx9x0').text.strip()
                except AttributeError:
                    price = "Нет цены"

                try:
                    # Извлекаем ссылку на объявление
                    link = ad.find('a', class_='g6gv8w4 g6gv8w8 _1ioeqy90')['href']
                except (AttributeError, TypeError):
                    link = "Нет ссылки"

                # Записываем данные в файл
                file.write(f'Заголовок: {title}\n')
                file.write(f'Цена: {price}\n')
                file.write(f'Ссылка: {link}\n')
                file.write('-' * 50 + '\n')

        print('Данные успешно записаны в файл car_ads.txt')
else:
    print(f'Ошибка при запросе к сайту: {response.status_code}')
