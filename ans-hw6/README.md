# Ansible Playbook for Installing ClickHouse, Vector, and Lighthouse

## Описание

Этот Ansible playbook автоматизирует установку и настройку трёх компонентов на Ubuntu-системах:

- ClickHouse (анализ данных)
- Vector (сборщик логов)
- Lighthouse + Nginx (веб-сервер и фронтенд)

Playbook состоит из трёх частей (play), каждая выполняется на своей группе хостов.

---

## Что делает playbook

### Play 1: Установка ClickHouse

- Устанавливает нужные зависимости
- Добавляет официальный GPG-ключ и репозиторий ClickHouse
- Устанавливает пакеты ClickHouse (client, server, common-static)
- Запускает сервис ClickHouse и создаёт базу данных `logs`

### Play 2: Установка Vector

- Устанавливает зависимости (curl, wget)
- Загружает и распаковывает бинарный файл Vector
- Копирует бинарник в `/usr/local/bin`
- Создаёт конфигурационный файл для отправки логов из `/var/log/syslog` в ClickHouse
- Настраивает systemd сервис для Vector и запускает его

### Play 3: Установка Lighthouse и Nginx

- Устанавливает Nginx и git
- Клонирует репозиторий Lighthouse из GitHub
- Настраивает владельца файлов
- Создаёт конфигурацию Nginx для обслуживания Lighthouse
- Проверяет конфигурацию Nginx и запускает сервис

---

## Параметры playbook

### Play 1 (ClickHouse)

- `clickhouse_version` — версия ClickHouse (по умолчанию: "22.3.3.44")
- `clickhouse_packages` — список пакетов для установки (clickhouse-client, clickhouse-server, clickhouse-common-static)

### Play 2 (Vector)

- `vector_version` — версия Vector (по умолчанию: "0.50.0")
- `vector_config_dir` — директория для конфигурации Vector (по умолчанию: `/etc/vector`)
- `vector_user` — пользователь для запуска Vector (по умолчанию: `vector`)

### Play 3 (Lighthouse)

- `lighthouse_repo` — URL репозитория Lighthouse (по умолчанию: `https://github.com/VKCOM/lighthouse.git`)
- `lighthouse_location` — путь для установки Lighthouse (по умолчанию: `/var/www/lighthouse`)
- `nginx_user_name` — пользователь Nginx (по умолчанию: `www-data`)

---

## Теги

В playbook не заданы конкретные теги, но для удобства можно добавить теги для отдельных play или задач при необходимости, например:

- `clickhouse` — установка ClickHouse
- `vector` — установка Vector
- `lighthouse` — установка Lighthouse/Nginx

---

![clickhouse install ok](./img/clickhous-install.jpg)

![clickhouse check ok](./img/clickhous-check.jpg)

![vector install ok](./img/vector-installed.jpg)

![lighthous + nginx install ok](./img/nginx-installed.jpg)
