# PersonVille || team 3
[![pipeline status](https://gitlab.crja72.ru/django/2026/spring/course/projects/team-3/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2026/spring/course/projects/team-3/-/commits/main)

[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com/)

**PersonVille** — психологическая игра-тест, основанная на модели личности «Большая пятёрка». Пользователь проходит тест, получает профиль характера и строит свой уникальный город, где каждая улица отражает определённую черту личности.
## Основные возможности

- Интерактивный психологический тест (15 вопросов)
- Определение черт характера на основе ответов
- Построение персонального города с улицами и домами
- Итоговый персонаж с описанием характера
- Экспорт результата в PNG-карточку
- Регистрация и авторизация пользователей
---

### Предварительные требования

- Python 3.11+
- Git

### Установка и запуск (dev-режим)

1. Клонируйте репозиторий

```bash
git clone https://gitlab.crja72.ru/django/2026/spring/course/projects/team-3
```

2. Перейдите в папку проекта

```bash
cd team-3
```

3. Создайте виртуальное окружение

Linux/macOS
```bash
python3 -m venv venv
```

Windows (PowerShell)

```Power Shell
python -m venv venv
```

4. Активируйте виртуальное окружение

Linux/macOS

```bash
source venv/bin/activate
```

Windows (PowerShell)

```Power Shell
.\venv\Scripts\Activate.ps1
```

5. Установите зависимости

```bash
pip install -r requirements/prod.txt
```

6. Настройте переменные окружения

```bash
cp template.env .env
```

7. Примените миграции

```bash
python manage.py migrate
```

8. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

9. Запустите сервер разработки

```bash
python manage.py runserver
```
---
После запуска сервер будет доступен по адресу:

- Сайт: http://127.0.0.1:8000/

- Админка: http://127.0.0.1:8000/admin/

---

#### Игровой процесс
**1. Входной тест**

Человек проходит тест из 15 пунктов. На каждый пункт он выбирает один из 5 вариантов — от «совсем не похоже» до «очень похоже».

**2. Построение города**

На основе ответов формируется профиль по 5 чертам личности (модель «Большая пятёрка»):
- Экстраверсия (Extraversion)
- Доброжелательность (Agreeableness)
- Добросовестность (Conscientiousness)
- Нейротизм (Negative Emotionality)
- Открытость опыту (Openness)

Каждая черта получает уровень: low, mid или high.

**3. Улицы и дома**

Для каждой черты создаётся улица с тремя домами. Каждый дом содержит уточняющий вопрос, на который пользователь выбирает один из пяти ответов — насколько это на него похоже.

**4. Итоговый персонаж**

После прохождения всех улиц формируется итоговый персонаж с описанием характера, который можно скачать в виде PNG-карточки.
---

#### Установка зависимостей

Для запуска тестов:

```bash
pip install -r requirements/test.txt
```

Для разработки:
```bash
pip install -r requirements/dev.txt
```

---
## Структура проекта
```
team-3/
├── person_ville/                # Основная директория проекта
│   ├── analytics/               # Сбор статистики
│   ├── city/                    # Логика города
│   ├── core/                    # Базовые модели
│   ├── homepage/                # Главная страница
│   ├── quizzes/                 # Логика тестов
│   ├── users/                   # Модель пользователя
│   ├── static_dev/              # Статика для разработки
│   ├── templates/               # HTML-шаблоны
│   ├── manage.py
├── requirements/                # Зависимости
├── .env.example                 # Пример переменных окружения
├── .flake8
├── pyproject.toml
├── .gitignore
├── .gitlab-ci.yml
└── README.md
```

---

## Схема базы данных
```mermaid
erDiagram
    User ||--o{ UserResultHistory : "имеет записи"
    User ||--o{ EmailChangeCode : "запрашивает код"
    User ||--o{ PasswordChangeCode : "запрашивает код"
    User ||--o{ CompletedQuizSession : "проходит квиз"

    User {
        int id PK
        datetime created_at "из BaseUpdate"
        datetime updated_at "из BaseUpdate"
        varchar username UK "уникальный"
        varchar email UK "уникальный"
        varchar password "хэшированный"
        varchar first_name "имя"
        varchar last_name "фамилия"
        varchar role "роль"
        varchar city "город"
        boolean is_email_verified "email подтвержден"
        boolean is_active "активен"
        boolean is_staff "персонал"
        boolean is_superuser "суперпользователь"
        datetime last_login "последний вход"
        datetime date_joined "дата регистрации"
        datetime email_change_cooldown_until "таймаут смены email"
        datetime password_change_cooldown_until "таймаут смены пароля"
    }

    UserResultHistory {
        int id PK
        int user_id FK
        varchar title "название"
        text short_summary "краткое описание"
        json snapshot "Город"
        datetime created_at "дата создания"
    }

    EmailChangeCode {
        int id PK
        int user_id FK
        varchar new_email "новый email"
        varchar code "6 символов"
        datetime created_at "дата создания"
        datetime expires_at "срок действия"
        datetime resend_available_at "доступность повторной отправки"
        boolean is_used "использован"
    }

    PasswordChangeCode {
        int id PK
        int user_id FK
        varchar new_password_hash "хэш нового пароля"
        varchar code "6 символов"
        datetime created_at "дата создания"
        datetime expires_at "срок действия"
        datetime resend_available_at "доступность повторной отправки"
        boolean is_used "использован"
    }

    CompletedQuizSession {
        int id PK
        varchar session_key "сессия прохождения"
        int user_id FK
        datetime started_at "начало"
        datetime completed_at "дата прохождения"
        int duration_seconds "длительность в секундах"
        json final_character "итоговый персонаж"
        datetime created_at "дата создания"
    }
```
---

---

### Разработчики

Студенты:
```
Светлана Зурова
Максим Чернов
Дмитрий Севостьянов
```

Курс: Django-разработка, 2026

---
