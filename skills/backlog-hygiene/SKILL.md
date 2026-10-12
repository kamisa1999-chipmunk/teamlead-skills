---
name: backlog-hygiene
description: >-
  Read-only аудит гигиены Jira-бэклога CAT2: мусор, зависшие задачи, лишние
  контейнеры в спринтах, потерянные Testing, история решений. Не планирует
  спринт и не меняет Jira. Используй при командах: backlog hygiene, гигиена
  бэклога, аудит бэклога, почистить Jira, лишние Epic в спринте, хвост
  тестирования, pre-sprint hygiene, deep audit бэклога.
---

# Backlog hygiene

## Назначение

Регулярно проверять Jira-бэклог и спринты: устаревшее, потерянное, лишнее, неправильно размещённое, требующее человеческого решения.

Это **не** sprint planner.

- `backlog-hygiene` — что в Jira выглядит мусором или требует решения
- `sprint-planning` — что взять в следующий спринт

Скрипты собирают факты. Скилл объясняет отчёт. **Jira не менять.** Рекомендации не записывать в историю решений без явного ответа пользователя.

## Триггеры

- «гигиена бэклога» / backlog hygiene
- «аудит бэклога» / deep audit
- «что почистить в Jira перед планированием»
- «лишние Epic в спринте»
- «хвост Testing» / потерянные задачи тестирования

Не путать со `sprint-planning`, `sprint-review`, `testing-monitor`, `jira-write`.

## CLI

```bash
pip3 install -r notes/jira/scripts/requirements.txt

python3 notes/jira/backlog_hygiene.py --mode deep
python3 notes/jira/backlog_hygiene.py --mode pre-sprint
python3 notes/jira/scripts/cli/backlog_hygiene.py --mode pre-sprint --project CAT2
```

Конфиг: `notes/jira/scripts/config/hygiene.yaml`  
Отчёты: `notes/jira/reports/backlog-hygiene/`  
История решений: `notes/jira/hygiene/baseline.yaml`

Имя файла: `{YYYY-MM-DD}__{PROJECT}__{deep|pre-sprint}.yaml` (+ `.md`).

Токен не читать и не показывать. Старые отчёты не перезаписывать.

## Когда ходить в Jira

| Ситуация | Действие |
|----------|----------|
| Есть отчёт **< 8 ч** того же режима | Читать YAML/Markdown, скрипт не запускать |
| Уточнение по тем же фактам | Тот же отчёт |
| Старше 8 ч или «обнови / пересобери» | Новый запуск CLI → **новый** файл |
| Первый запуск / давно не смотрели / захламлён backlog | `--mode deep` |
| Перед планированием спринта | `--mode pre-sprint` |

## Что показать в ответе

1. Русский Markdown-отчёт (как есть; ссылка = ключ + название задачи)
2. Коротко: режим, текущий спринт, сколько скрыто историей решений
3. Ограничения из отчёта — не скрывать дыры в данных
4. Путь к YAML

Не вываливать весь YAML. Не предлагать закрыть задачу только из‑за возраста.

Подтверждённые действия в Jira — отдельно через `jira-write` после явного «примени».

## История решений

Сам факт рекомендации **не** писать в baseline.

После явного ответа («CAT2-945 оставляем, но из спринта убираем»):

```bash
python3 notes/jira/backlog_hygiene.py --record-decision CAT2-945 \
  --action KEEP --allow-in-sprint false --keep-issue true \
  --note "Epic-контейнер, не таскать по спринтам"
```

Допустимые `--action`: `KEEP`, `REMOVE_FROM_SPRINT`, `CLOSE_CANDIDATE`, `CANCEL_CANDIDATE`, `NEEDS_OWNER`, `NEEDS_PRODUCT_DECISION`, `MERGE_OR_SUPERSEDED`, `INVESTIGATE`, `MOVE_TO_BACKLOG`, `REVIEW_LATER`.

## Чего не делать

- Не менять Jira (статус, sprint, assignee, labels, parent, описание)
- Не менять planning Phase 1.5 / `planning/`
- Не интегрировать результат в sprint-planning
- Не ходить в Jira issue-by-issue, если поле уже есть в отчёте
- Не считать «нет в notes» основанием закрыть задачу

Правила сигналов, рекомендаций и fingerprint: [reference.md](reference.md).
