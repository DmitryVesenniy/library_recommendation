# Инструкция по сборке сервиса library_recommendation
____

*Для сборки приложения вам потребуется установленный пакет Python 3.9 или выше.*
### `https://www.python.org/downloads/`

**Создаем виртуальное окружение и устанавливаем все зависимости:** 
### `setup.sh`

**В корне проекта лежит файл конфигурации config.ini:** 
### `очень важно прописать пути до датасетов. Переменные: DATA_SET_PATH, BOOKS_DATA_JSN`

**Запуск обучающейся модели:** 
### `start_train.sh`

Обучение может занять продолжительное время, если флаг CALCULATE_ALL = True, то обучение займет до 30 часов.
В случае установки CALCULATE_ALL = False, обучение будет длиться ~ 30минут.

# Структура проекта

### `recommendation` - Все, что связанно с обучающейся моделью
### `api` - Сервис API

### АПИ
`response: /recommendation POST {id: number}`
`request: {recommendation: Array<{id: number, title: string}>, history: Array<{id: number, title: string}>}`

### DATASET
`https://disk.yandex.ru/d/jG-LLWB37O-G3w`
