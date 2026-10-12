# YAML расписания квартала

Писать в `features/<quarter>-schedule.yaml`. Команды — из корня репозитория `notes`.

## Корень

```yaml
title: Q4 2026 CAT2
quarter: Q4-2026
from: 2026-10-01
to: 2026-12-31
holidays: ["2026-11-04"]
planning:
  goal: maximize_priority   # must | minimize_dates | check_basket | even_load
releases:
  - { version: "6.20", date: 2026-10-12 }
size_days:
  XS: 2
  S: 3
  M: 5
  L: 10
  XL: 15
people: []
items: []
```

`from` / `to` — окно. Работа, которая не заканчивается в окне, попадает в `unscheduled` (`outside_quarter`). `holidays` — нерабочие дни помимо выходных.

`planning.goal`:

- `maximize_priority` — больше приоритетных фич
- `must` — сначала must
- `minimize_dates` — короче календарь
- `check_basket` — что из всей корзины влезает
- `even_load` — ровнее загрузка людей

## Люди (`people`)

Если блок есть, анонимного слота нет: нет исполнителя на дорожке → `unscheduled` / `no_resource`.

```yaml
people:
  - id: maxim
    name: Максим
    lanes: [ios]
    share: [android]          # backup, не основная ёмкость
    capacity: 1.0             # фактическая сейчас; не ставить 0.5 из кадрового риска
    time_off:
      - { from: 2026-09-01, to: 2026-09-14 }   # причина в Гант не выводится
    risks:
      - { type: leave_risk }  # отдельный сценарий, не режет текущую ёмкость
```

`who` на баре должен быть в `lanes` или `share`. Архивные карточки в `people` не класть.

## Фича

```yaml
- id: Q4-04
  title: Переход на все товары
  jira: CAT2-1370
  must: false
  priority: 80
  value: 50
  order_hint: 0
  target_release: "6.22"
  depends_on: [Q4-11]
  kind: development          # research — не выдавать за оценённую разработку
  bars:
    - { lane: ios, days: 8 }
    - { lane: android, min_days: 8, max_days: 15 }
    - { lane: web, estimate_status: unknown, contingent: true }
```

Неизвестный `depends_on` и цикл — ошибка планировщика, не молчаливый skip.

## Оценка бара

| Состояние | Поля |
|-----------|------|
| точная | `days` или `hours` или `size: M` |
| диапазон | `min_days`+`max_days` или `size: L-XL` |
| неизвестна | `estimate_status: unknown` (не подставлять S) |

Сценарии для диапазона: `optimistic` = min, `pessimistic` = max, `base` = середина и пометка `hypothesis`.

`kind: research` + дальнейшая разработка `contingent: true` + `unknown` — сначала research, разработка в «не оценено».

Несколько баров одной `lane` в одной фиче допустимы (идут подряд).

Ручные `start`/`end` проверяются: пересечение одного человека — ошибка; даты вне окна — `unscheduled`.

## Дорожки

`sa` · `backend` · `admin` · `web` · `ios` · `android` · `design` · `test` · `external`

Порядок этапов внутри фичи: SA/research → backend → платформы → тест.

## CLI

```bash
pip3 install -r features/gantt/requirements.txt
python3 features/gantt/fill_dates.py --input features/demo-schedule.yaml
python3 features/gantt/render_gantt.py --input features/gantt-runs/<папка>/yaml/base.yaml --output features/gantt-runs/<папка>
```

Каждый прогон — папка: `yaml/` (расписание), `html/gantt-features.html` (по фичам), `html/gantt-people.html` (по людям), `report.md`. Указатель последнего: `features/gantt-runs/LATEST.md`. Mermaid не используется.

Без `--output` yaml пишется в новую папку `features/gantt-runs/<время>__<quarter>/`. Существующий yaml чужого прогона не перезаписывать, если не указан `--output`. Картинки того же прогона обновлять `render_gantt.py` можно — это не пересчёт плана.
