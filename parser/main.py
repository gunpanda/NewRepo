import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_html(product_name):
    # Настройки для Selenium
    options = Options()
    options.add_argument('--headless')  # Запуск в фоновом режиме
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

    # Пример использования прокси (замените на свой прокси)
    # options.add_argument('--proxy-server=http://your_proxy_address:port')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Wildberries
        wb_url = f"https://www.wildberries.ru/catalog/search.aspx?search={product_name}"
        driver.get(wb_url)
        time.sleep(random.uniform(15, 30))  # Увеличено время ожидания

        # Прокрутка страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))

        # Получаем HTML-код страницы
        wb_html = driver.page_source
        with open('wildberries_output.html', 'w', encoding='utf-8') as f:
            f.write(wb_html)  # Сохраняем HTML для анализа

        # Ozon
        ozon_url = f"https://www.ozon.ru/search/?text={product_name}&from_global=true"
        driver.get(ozon_url)
        time.sleep(random.uniform(15, 30))  # Увеличено время ожидания

        # Прокрутка страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))

        # Получаем HTML-код страницы
        ozon_html = driver.page_source
        with open('ozon_output.html', 'w', encoding='utf-8') as f:
            f.write(ozon_html)  # Сохраняем HTML для анализа

        print("HTML сохранен для Wildberries и Ozon.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()  # Закрыть браузер

# Пример использования
product_name = "часы"  # Замени на нужное название товара
get_html(product_name)
