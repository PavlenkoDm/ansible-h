# Ansible Playbook: ClickHouse + Vector + Lighthouse Stack

[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

## Описание

Этот Ansible playbook автоматизирует развертывание полного стека для сбора, хранения и визуализации логов на Ubuntu-системах:

- **ClickHouse** - высокопроизводительная колоночная СУБД для аналитики
- **Vector** - сборщик и обработчик логов
- **Lighthouse** - веб-интерфейс для мониторинга и визуализации данных в ClickHouse

Playbook использует модульную архитектуру на основе **Ansible Roles**, что обеспечивает:

- ✅ Переиспользуемость компонентов
- ✅ Простоту поддержки и обновления
- ✅ Изоляцию конфигурации каждого сервиса
- ✅ Возможность независимого версионирования ролей

---

## Архитектура решения

```
┌─────────────────┐
│   Lighthouse    │  ← Веб-интерфейс (порт 80)
│   + Nginx       │
└────────┬────────┘
         │
         │ (Queries)
         ▼
┌─────────────────┐
│   ClickHouse    │  ← Хранилище логов (порт 9000)
│   Database      │
└────────▲────────┘
         │
         │ (Logs)
         │
┌────────┴────────┐
│     Vector      │  ← Сборщик логов
│  Log Collector  │     (читает /var/log/syslog)
└─────────────────┘
```

---

## Требования

### Система управления (Control Node)

- Ansible >= 2.12
- Git (для клонирования ролей)
- SSH доступ к целевым хостам
- Python 3.x

### Целевые хосты (Managed Nodes)

- Ubuntu 22.04 (Jammy) или Ubuntu 20.04 (Focal)
- Права sudo для пользователя
- Открытые порты:
  - ClickHouse: `9000` (TCP), `8123` (HTTP)
  - Vector: не требует открытых портов (клиент)
  - Lighthouse: `80` (HTTP) или кастомный порт

---

## Структура проекта

```
playbook/
├── inventory/
│   └── prod.yml              # Inventory с хостами
├── roles/                    # Роли (скачиваются из GitHub)
│   ├── clickhouse/
│   ├── vector/
│   └── lighthouse/
├── requirements.yml          # Зависимости ролей
├── site.yml                  # Основной playbook
└── README.md                 # Документация
```

---

## Используемые роли

Все роли размещены в отдельных репозиториях:

| Роль           | Репозиторий                                                      | Версия | Назначение                     |
| -------------- | ---------------------------------------------------------------- | ------ | ------------------------------ |
| **clickhouse** | [clickhouse-role](https://github.com/PavlenkoDm/clickhouse-role) | 1.0.0  | Установка ClickHouse СУБД      |
| **vector**     | [vector-role](https://github.com/PavlenkoDm/vector-role)         | 1.0.0  | Установка Vector log collector |
| **lighthouse** | [lighthouse-role](https://github.com/PavlenkoDm/lighthouse-role) | 1.0.0  | Установка Lighthouse + Nginx   |

---

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <your-repo-url>
cd playbook
```

### 2. Настройте inventory

Отредактируйте `inventory/prod.yml` и укажите IP адреса ваших серверов:

```yaml
all:
  vars:
    ansible_connection: ssh
    ansible_user: ubuntu
    ansible_ssh_private_key_file: /root/.ssh/id_ed25519

  children:
    clickhouse:
      hosts:
        clickhouse-01:
          ansible_host: <IP_CLICKHOUSE>

    vector:
      hosts:
        vector-01:
          ansible_host: <IP_VECTOR>

    lighthouse:
      hosts:
        lighthouse-01:
          ansible_host: <IP_LIGHTHOUSE>
```

### 3. Установите зависимости (роли)

```bash
ansible-galaxy install -r requirements.yml -p roles/ --force
```

**Что происходит:**

- Ansible скачивает роли из GitHub
- Устанавливает версию `1.0.0` каждой роли
- Сохраняет в папку `roles/`

### 4. Проверьте доступность хостов

```bash
ansible all -i inventory/prod.yml -m ping
```

Должен вернуться `pong` от всех хостов.

### 5. Запустите playbook

```bash
# Проверка синтаксиса
ansible-playbook -i inventory/prod.yml site.yml --syntax-check

# Dry-run (проверка без применения)
ansible-playbook -i inventory/prod.yml site.yml --check

# Реальное выполнение
ansible-playbook -i inventory/prod.yml site.yml
```

---

## Конфигурация

### Переменные ClickHouse

Роль устанавливает ClickHouse со следующими параметрами по умолчанию:

```yaml
clickhouse_version: "22.3.3.44"
clickhouse_packages:
  - clickhouse-client
  - clickhouse-server
  - clickhouse-common-static
clickhouse_database: "logs"
```

**Переопределение в playbook:**

```yaml
roles:
  - role: clickhouse
    vars:
      clickhouse_database: "my_custom_db"
```

**Документация роли:** [clickhouse-role README](https://github.com/PavlenkoDm/clickhouse-role)

---

### Переменные Vector

Роль настраивает Vector для отправки логов в ClickHouse:

```yaml
vector_version: "0.50.0"
vector_config_dir: /etc/vector
vector_clickhouse_host: "127.0.0.1"
vector_clickhouse_port: 9000
vector_clickhouse_database: "logs"
vector_clickhouse_table: "events"
```

**Важно:** В playbook `vector_clickhouse_host` динамически получается из inventory:

```yaml
vector_clickhouse_host: "{{ hostvars['clickhouse-01']['ansible_host'] }}"
```

**Документация роли:** [vector-role README](https://github.com/PavlenkoDm/vector-role)

---

### Переменные Lighthouse

Роль устанавливает Lighthouse с Nginx:

```yaml
lighthouse_repo: "https://github.com/VKCOM/lighthouse.git"
lighthouse_location: "/var/www/lighthouse"
lighthouse_nginx_manage: true
lighthouse_nginx_port: 80
lighthouse_nginx_user: "www-data"
```

**Документация роли:** [lighthouse-role README](https://github.com/PavlenkoDm/lighthouse-role)

---

## Использование

### Установка всего стека

```bash
ansible-playbook -i inventory/prod.yml site.yml
```

### Установка отдельного компонента

```bash
# Только ClickHouse
ansible-playbook -i inventory/prod.yml site.yml --limit clickhouse

# Только Vector
ansible-playbook -i inventory/prod.yml site.yml --limit vector

# Только Lighthouse
ansible-playbook -i inventory/prod.yml site.yml --limit lighthouse
```

### Использование тегов

```bash
# Все задачи с тегом clickhouse
ansible-playbook -i inventory/prod.yml site.yml --tags clickhouse

# Все задачи с тегами vector и lighthouse
ansible-playbook -i inventory/prod.yml site.yml --tags "vector,lighthouse"

# Пропустить установку Lighthouse
ansible-playbook -i inventory/prod.yml site.yml --skip-tags lighthouse
```

---

## Проверка работоспособности

### ClickHouse

```bash
# На сервере ClickHouse
clickhouse-client -q "SHOW DATABASES;"
# Должна быть база 'logs'

clickhouse-client -q "SELECT version();"
# Проверка версии
```

### Vector

```bash
# На сервере Vector
systemctl status vector

# Проверка логов
journalctl -u vector -n 50

# Проверка конфигурации
/usr/local/bin/vector validate /etc/vector/vector.toml
```

### Lighthouse

```bash
# На сервере Lighthouse
systemctl status nginx

# Проверка файлов
ls -la /var/www/lighthouse

# Проверка из браузера
curl http://<lighthouse-ip>
```

**Веб-интерфейс:**
Откройте в браузере: `http://<lighthouse-server-ip>`

---

## Обновление ролей

### Обновление до новой версии

1. Измените версию в `requirements.yml`:

```yaml
- src: git@github.com:PavlenkoDm/clickhouse-role.git
  version: "1.1.0" # Новая версия
```

2. Переустановите роли:

```bash
ansible-galaxy install -r requirements.yml -p roles/ --force
```

3. Запустите playbook:

```bash
ansible-playbook -i inventory/prod.yml site.yml
```

---

## Устранение неполадок

### Ошибка: "Role not found"

**Проблема:** Роли не скачались из GitHub.

**Решение:**

```bash
# Проверьте SSH доступ к GitHub
ssh -T git@github.com

# Переустановите роли
ansible-galaxy install -r requirements.yml -p roles/ --force
```

---

### Ошибка: Vector не может подключиться к ClickHouse

**Проблема:** Неправильный IP адрес ClickHouse или firewall блокирует порт 9000.

**Решение:**

1. Проверьте доступность ClickHouse:

```bash
telnet <clickhouse-ip> 9000
```

2. Проверьте переменную в playbook:

```yaml
vector_clickhouse_host: "{{ hostvars['clickhouse-01']['ansible_host'] }}"
```

3. Проверьте firewall на сервере ClickHouse:

```bash
sudo ufw status
sudo ufw allow 9000/tcp
```

---

### Ошибка: Lighthouse показывает 403 Forbidden

**Проблема:** Неправильные права на файлы.

**Решение:**

```bash
# На сервере Lighthouse
sudo chown -R www-data:www-data /var/www/lighthouse
sudo chmod -R 755 /var/www/lighthouse
sudo systemctl restart nginx
```

---

## Дополнительная настройка

### Настройка firewall

```yaml
# Добавьте в playbook задачи для ufw
- name: Configure firewall
  hosts: all
  become: yes
  tasks:
    - name: Allow SSH
      ufw:
        rule: allow
        port: 22

    - name: Allow ClickHouse
      ufw:
        rule: allow
        port: 9000
      when: "'clickhouse' in group_names"

    - name: Allow HTTP for Lighthouse
      ufw:
        rule: allow
        port: 80
      when: "'lighthouse' in group_names"
```

### Настройка мониторинга

Для production рекомендуется добавить:

- Prometheus для мониторинга метрик
- Grafana для визуализации
- Alertmanager для алертов

---

## Безопасность

⚠️ **Рекомендации:**

1. **Используйте Ansible Vault для секретов:**

```bash
ansible-vault create secrets.yml
```

2. **Настройте firewall** (см. раздел выше)

3. **Используйте HTTPS для Lighthouse:**

   - Установите Let's Encrypt сертификат
   - Настройте Nginx для SSL

4. **Ограничьте доступ к ClickHouse:**

   - Настройте пользователей и права
   - Используйте strong passwords

5. **Регулярно обновляйте компоненты:**

```bash
# Обновите версии в requirements.yml
ansible-galaxy install -r requirements.yml -p roles/ --force
```

---

## Версионирование

Проект использует семантическое версионирование для ролей:

- **MAJOR** (1.x.x) - несовместимые изменения
- **MINOR** (x.1.x) - новая функциональность
- **PATCH** (x.x.1) - исправления багов

Текущие версии ролей: **1.0.0**

---

## Лицензия

MIT

---

## Автор

Dmitry Pavlenko  
GitHub: [@PavlenkoDm](https://github.com/PavlenkoDm)

---

## Ссылки

### Роли проекта

- [ClickHouse Role](https://github.com/PavlenkoDm/clickhouse-role)
- [Vector Role](https://github.com/PavlenkoDm/vector-role)
- [Lighthouse Role](https://github.com/PavlenkoDm/lighthouse-role)

### Официальная документация

- [Ansible Documentation](https://docs.ansible.com/)
- [ClickHouse Documentation](https://clickhouse.com/docs)
- [Vector Documentation](https://vector.dev/docs/)
- [Lighthouse GitHub](https://github.com/VKCOM/lighthouse)

### Полезные ресурсы

- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
