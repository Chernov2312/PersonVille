# PersonVille || team 3
[![pipeline status](https://gitlab.crja72.ru/django/2026/spring/course/projects/team-3/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2026/spring/course/projects/team-3/-/commits/main)

[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)](https://getbootstrap.com/)


**PersonVille** — психологическая игра-тест, основанная на модели личности «Большая пятёрка». Пользователь проходит тест, получает профиль характера и строит свой уникальный город, где каждая улица отражает определённую черту личности.
## Основные возможности

- Интерактивный психологический тест (опросник)
- Определение черт характера на основе ответов 
- Построение персонального города (графика + описание)

## Быстрый старт
### Предварительные требования

- Python 3.10 или выше
- pip
- virtualenv

### Установка

```bash
# 1. Клонируйте репозиторий
git clone https://gitlab.crja72.ru/django/2026/spring/course/projects/team-3
cd person_ville

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте виртуальное окружение
# Windows:
./venv/Scripts/activate
# macOS / Linux:
source venv/bin/activate

# 4. Установите зависимости для разработки
pip install -r requirements/dev.txt

# 5. Создайте файл .env на основе примера
cp .env.example .env
# Отредактируйте .env, укажите SECRET_KEY

# 6. Примените миграции
python manage.py migrate

# 7. Создайте суперпользователя
python manage.py createsuperuser

# 8. Запустите сервер разработки
python manage.py runserver

Откройте http://localhost:8000 в браузере.
```


## Игровой процесс
**1. Входной тест**

Пользователь отвечает на 15 вопросов, оценивая утверждения по шкале от 1 до 5.

**2. Построение города**

На основе ответов формируется профиль по 5 чертам личности (модель «Большая пятёрка»):
- Экстраверсия (Extraversion)
- Доброжелательность (Agreeableness)
- Добросовестность (Conscientiousness)
- Нейротизм (Negative Emotionality)
- Открытость опыту (Openness)
Каждая черта получает уровень: low, mid или high.

**3. Улицы и дома**

Для каждой черты создаётся улица с тремя домами. Каждый дом содержит уточняющее утверждение, которое пользователь может принять или отвергнуть.

**4. Итоговый персонаж**

После прохождения всех улиц формируется итоговый персонаж с описанием характера, который можно скачать в виде PNG-карточки.