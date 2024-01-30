# Сервис "Робо QA"

```shell
poetry install
poetry shell
```

```shell
poetry run uvicorn roboqa_web.main:app --reload
```

### Функции

- [ ] API для получения простого фидбека
- [ ] Интеграция с беклогом доски на github
- [ ] Оповещение в telegram dev-группу проекта
- [ ] Напоминание о дежурстве для ручного прогона use case'ов

### Конфигурация

```toml
[integrations.telegram]
api_key = ''
group_id = 0

[integrations.github]
api_key = ''

[integrations.github.project]
owner = ''
project_id = 0
project_node = ''

[jobs.daily_duty]
cron = '0,30 09,16 * * 1-5'
```
