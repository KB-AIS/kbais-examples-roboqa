# Сервис "Робо QA"

## Функции

- [ ] API для регистрации сообщения о проблеме
- [ ] Интеграция с беклогом на github
- [ ] Оповещение в telegram группу проекта
- [ ] Напоминание о дежурстве для ручного прогона use case'ов

## Требования

- `python` ^3.11
- `Docker` (для запуска в `docker-compose`)

## Запуск

#### Для локальной разработки

```shell
poetry install
poetry shell
```

#### Запуск в docker-compose

Создать файл `config.toml` с требуемыми параметрами [конфигурации](#конфигурация).

Запустить проект через `docker-compose`:

```shell
docker-compose -f "./manifests/docker-compose.yml" -p kba-exa-roboqa up -d
```

#### Команды запуска

Из виртуальной среды созданной `poetry`

Сервис фоновых задач

```shell
dramatiq roboqa_web.runners.tasks:run
````

Сервис REST API

```shell
python -m roboqa_web.runners.api
```

Сервис телеграмм-бота

```shell
python -m roboqa_web.runners.bot
```

#### Конфигурация

Осуществляется через файл `config.toml` в директории запуска модулей

```toml
[infrastructure.data]
# Строка подключения к Redis
redis_url = 'redis://localhost:6379'

[integrations.telegram]
# Ключ доступа к Telegram Bot API
api_key = ''
# Идентификатор группы (chat_id) для отправки сообщений о проблеме
group_id = 0

[integrations.github]
# Ключ доступа к Github GraphQL API
api_key = ''

[integrations.github.project]
# Владелец доски, используется для формирования URL
owner = 'orgs/EXAMPLE'
# Идентификатор доски владельца`, используется для формирования URL
project_id = 0
# Идентификатор доски на API 
project_api_id = ''

[jobs.remind_duty]
# CRON выражения для регулярной задачи "Напоминание о Дежурстве"
cron = '0,30 09,16 * * 1-5'
```
