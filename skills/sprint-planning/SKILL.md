---
name: sprint-planning
description: >-
  Планирование спринта CAT2: snapshot, проверка готовности и черновик
  следующего спринта. Используй при командах: подготовь следующий спринт,
  planning snapshot, снимок перед планированием, проверь готовность к
  планированию, pre-planning, validate sprint planning, plan sprint,
  черновик спринта. Не пишет в Jira без отдельного явного подтверждения.
---

# Sprint planning

Пользователь не обязан знать фазы. Главная команда: **«Подготовь следующий спринт»**.

Внутри:

snapshot → hygiene → preplanning → questions → draft → правки → Jira preview → запись отдельно

LLM **не** собирает факты из Jira вручную, если их можно получить скриптом.

> Scripts collect facts. Skill interprets facts and user language.

Jira **не писать** из этого скилла. Preview — да. Apply — только отдельным шагом через существующий write-слой после явного «применяй».

## Что не путать

- `backlog-hygiene` — что в Jira выглядит мусором
- Phase 2 — что мешает планировать
- Phase 3 — рекомендуемый черновик следующего спринта
- `sprint-review` / `sprint-management` — ход спринта и создание спринта в Jira

---

# Phase 3: черновик следующего спринта

## Триггеры

- «Подготовь следующий спринт»
- «черновик спринта»
- «plan sprint»
- «sprint-planning phase 3»

## Как работать

1. Если snapshot **< 8 ч** — читать его. Иначе собрать Phase 1.5.
2. Если preplanning **< 8 ч** — читать его. Иначе прогнать Phase 2.
3. Запустить Phase 3. Планирование **не завершено**, пока по очереди не пройдены:

   carry-over / уже начатая работа → кандидаты ближайшего релевантного planning period → подтверждение feature scope → QA-план → ёмкость → при понятной свободной ёмкости R2D / FT / tech debt → итоговый planning artifact → Jira preview.

   Preview не добавляет новые фичи впервые и не строит QA впервые. Missing task / missing estimate — unresolved/action item, не повод уходить в Jira create/write.

```bash
python3 notes/jira/plan_sprint.py
python3 notes/jira/plan_sprint.py --text "Максима на Android не ставь"
python3 notes/jira/plan_sprint.py --session <file> --text "ок"
```

CLI только для debug. В чате не заставлять пользователя запускать несколько команд.

4. Показать пользователю **1–2 вопроса** из вывода. Не вываливать внутренние enums (`work_role`, `planning_lane`, `READY_NOW`).
5. После ответа — снова скрипт с `--text` / продолжить session. Пересчитать очередь. Не задавать вопросы, которые стали неактуальны.
6. Когда появился черновик — показать **краткое summary** и путь к planning artifact. Artifact — основной итог: фичи, люди, регрессы, QA-пакеты/очередь, риски, needs_task, оценки, сообщение команде.
7. Правки обычным русским: «не бери CAT2-…», «отдай Руслану», «оставь 15% резерва», «добавь техдолг». После правки показать **diff**, не весь план. Подтверждённые решения — facts, их не пересчитывать эвристикой.
8. На «ок» / «план готов» — только если artifact уже есть: показать Jira preview существующих задач. **Не вызывать write. Не заводить missing task до конца planning flow.**
9. Спросить «Применить изменения?» и остановиться.

Сессии: `notes/jira/reports/planning-sessions/` (в git не класть).

## Вопросы

Порядок: нет исполнителя на обязательную работу → неясная роль обязательной → дедлайн → просроченный регресс → **конфликт owner / неоднозначная Jira-задача регресса** → устаревший planning period → **нет графика mobile regression** → Android → незакрытый SA vs параллельная разработка → BA/unknown analysis → нет задач по ожидаемому направлению фичи → неясный следующий этап → missing estimate **только по задачам черновика** → зависимости.

Не спрашивать, нужен ли обязательный Web PLP regression. Если policy required — регресс в плане, даже без Jira-задачи. Отсутствующая задача обязательного регресса — warning/action item в черновике, не вопрос и не blocker сессии. Не спрашивать «не хватает оценок по 31 задаче». Сначала внутренний scope-кандидат, потом вопрос только по тем, кто реально попал в draft.

Feature-вопросы имеют высокий приоритет, если без них нельзя корректно собрать draft: параллельный старт при открытом SA, missing task, unknown next stage, stale planning period.

Общего лимита на число вопросов нет. За шаг — максимум 2.

«не знаю, пропусти» → безопасный default: не считать обязательной, не назначать автоматически, не выдумывать оценку.

## Черновик

Один рекомендуемый вариант. Альтернативы — только если пользователь явно попросил.

Приоритет выбора (не один numeric score):

явные решения пользователя → жёсткий/legal срок → commitment → обязательная работа → активный carry-over → **регулярные regression obligations (даже без Jira-задачи)** → **кандидаты фич и их этапы (SA / разработка / тест / mix)** → ready development → ready QA → backfill.

Порядок QA: фиксированные регрессы → уже начатый тест → feature testing пакетами → ready-now → overflow → automation в остатке. Регрессы остаются календарными слотами. Feature testing не планировать как `1 Testing issue = 1 день`. Testing задачи Chanel / логобара — один пакет: один owner, один прогон по готовности полного пакета, закрытие пачкой. QA показывает очередь/пакеты/риски, не искусственный календарь по карточке в день.

Фича сначала **кандидат**. Membership в schedule активного planning period достаточна, даже без numeric priority. `planned=true` только если в draft попал хотя бы один её work item. Не ставить planned только потому, что Story понравилась алгоритму. Cap на число новых фич нет.

Если спринт пересекает начало следующего planning period, новые feature candidates этого периода рассматривать. Для 21.09–02.10 Q4 нельзя игнорировать только потому, что период формально начинается 01.10.

Незавершённый SA не блокирует разработку автоматически — спросить, можно ли идти параллельно. Missing task не выдумывает часы и не выключает Ready to Development; делает ёмкость uncertain и отключает automatic backfill по человеку. Работа без Jira может быть `planned=true`, `needs_task=true`. Создавать такие задачи — только после подтверждения плана, блок «Нужно завести после подтверждения плана».

Единица продуктового планирования — Jira Story / DeliveryStory. Источник плана периода — `planning_periods` в config (`schedule` + `candidate_label`). Collectors берут active period, а не зашитый `features/q4-2026-schedule.yaml`. `notes.schedule` / `analysis.candidate_label` — только fallback. Если следующий спринт вне активного period — warning/вопрос, старый schedule молча не использовать.

Максима на Android **не назначать** без явного разрешения. Testing Android не зависит от доступности Ольги. BA и unknown Analysis не назначать Марии. SA — только системный анализ, без искусственных часов. Testing — очередь QA (Настя preferred, Костя overflow и backend). Owner регулярного регресса берётся из `regression_obligations` policy и может быть переназначен; generic QA preference ниже explicit regression owner.

Цифры capacity считает скрипт, не LLM. Для разработчиков источник — `capacity.developer_productive_hours_per_sprint: 60` на полный двухнедельный спринт, масштабируется рабочими днями. SA/QA эту норму не получают. Не пересчитывать как 8ч/день минус meeting overhead.

Явный запрос «добавь техдолг» берёт только техдолг и очистку feature toggle. Если подходящего нет — сказать об этом и предложить bug отдельно, не подставляя баг молча.

Если задача уже назначена на человека вне planning-team, исполнителя не менять автоматически. Сохранить внешнего assignee и спросить, если задача в плане.

## Чего не делать в Phase 3

- Не писать в Jira и не создавать спринт
- Не строить варианты A/B / conservative/aggressive
- Не показывать все вопросы сразу
- Не назначать Максима на Android молча
- Не отдавать BA/unknown Марии
- Не считать Testing ёмкостью разработчика
- Не применять developer 60ч к SA/QA и не считать ёмкость как 8ч − meetings
- Не расширять «добавь техдолг» до багов
- Не переназначать задачи с внешним assignee на нашу команду
- Не выдумывать даты mobile regression (odd/even week запрещены)
- Не отменять обязательный регресс из-за отсутствия Jira-задачи
- Не запускать deep hygiene внутри каждого pass

---

# Phase 1.5: Planning Snapshot

## Триггеры

- «Собери planning snapshot»
- «Факты к планированию спринта»
- «Снимок перед планированием»
- «sprint-planning phase 1»

## CLI

```bash
pip3 install -r notes/jira/scripts/requirements.txt

python3 notes/jira/build_planning_snapshot.py
python3 notes/jira/build_planning_snapshot.py --current-dates 07.09-18.09
```

Отчёты: `notes/jira/reports/planning-snapshot/` (старые не перезаписывать).

Если snapshot **< 8 ч** — читать его, скрипт не запускать.

## Чего не делать в Phase 1.5

- Не выбирать задачи и не считать priority score
- Не балансировать людей
- Не менять Jira / notes
- Не запускать Phase 2 автоматически, если просили только snapshot

---

# Phase 2: проверка готовности и pre-planning

## Триггеры

- «проверь готовность к планированию»
- «pre-planning»
- «validate sprint planning»
- «что мешает планировать спринт»
- «Phase 2»

## CLI

```bash
python3 notes/jira/validate_sprint_planning.py \
  --snapshot notes/jira/reports/planning-snapshot/<file>.yaml

python3 notes/jira/validate_sprint_planning.py \
  --snapshot <file>.yaml \
  --hygiene notes/jira/reports/backlog-hygiene/<file>.yaml
```

Если `--snapshot` не указан — берётся последний snapshot.
Если `--hygiene` не указан — подхватывается последний hygiene-отчёт и `jira/hygiene/baseline.yaml`, если они есть.

Отчёты: `notes/jira/reports/preplanning/` (в git не класть).

## Что показать в ответе

1. Русский Markdown-отчёт (как есть, ключи кликабельные)
2. Статус: можно планировать / с оговорками / нужны решения / вход битый
3. Что сознательно **не** считается критичным
4. Путь к YAML

Не вываливать весь YAML.

Если пользователь сразу сказал «подготовь следующий спринт» — после Phase 2 **продолжить Phase 3**, не останавливаться.

## Чего не делать в Phase 2

- Не составлять план спринта и не балансировать capacity
- Не строить QA-календарь
- Не двигать Jira, не создавать Analysis, не назначать людей
- Не дублировать backlog-hygiene
- Не считать неподтверждённую рекомендацию гигиены решением
- Не придумывать ёмкость SA/QA и оценки
- Не считать любой Analysis системным анализом
- Не назначать Testing на разработчиков по `[Back]` / `[IOS]` / `[Android]`

Детали схемы: [reference.md](reference.md).
