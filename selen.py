from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

# Функция для безопасного формирования имени файла
def safe_filename(query):
    # Заменяем недопустимые символы на "_"
    return re.sub(r'[<>:"/\\|?*]', '_', query)

driver = webdriver.Chrome()

try:
    driver.get("https://ru.wikipedia.org/w/index.php?search=&title=Служебная:Поиск&profile=advanced&fulltext=1&ns0=1")
    
    search_box = driver.find_element(By.ID, "ooui-php-1")
    
    # Вводим запрос
    search_query = "Хафизов"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Ждем, пока страница загрузится
    time.sleep(2)
    
    results = []

    search_results = driver.find_elements(By.CLASS_NAME, "mw-search-result-heading")

    for heading in search_results:
        title = heading.find_element(By.TAG_NAME, "a").text
        
        description_element = heading.find_element(By.XPATH, "following-sibling::div[contains(@class, 'searchresult')]")
        description = description_element.text.strip() if description_element else "Нет описания"        
        
        results.append({"title": title, "description": description})

    filename = f"{safe_filename(search_query)}.csv"

    # Сохраняем результаты в CSV файл
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "description"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Результаты сохранены в файл {filename}")

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Закрываем драйвер
    driver.quit()
