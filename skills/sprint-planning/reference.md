# Planning snapshot — reference (Phase 1.5 + Phase 2)

Скрипты в `notes/jira/scripts/planning/`. Skill интерпретирует YAML, не собирает Jira руками.
Phase 2 читает `planning_input`, а не 30k строк сырого snapshot.

## Структура

```text
notes/jira/scripts/
  config/planning.yaml
  planning/
    snapshot.py
    planning_input.py
    candidates.py
    roles.py
    features.py
    constraints.py
    qa_work_type.py
    regressions.py
    collectors/
    validation/          # Phase 2
  cli/build_planning_snapshot.py
  cli/validate_sprint_planning.py
```

## Schema (верхний уровень)

```yaml
generated_at:
phase: 1.5
sprint: { current, planning }
team:
planning_window:
current_sprint:          # полная картина спринта
carry_over:              # legacy: все незакрытые, включая containers
carry_over_work_items:   # только planning_role=work_item
carry_over_context:      # Epic / DeliveryStory / Release
ready_for_development:
planning_candidates:
qa:
  queue:                 # raw
  readiness:             # test↔dev, сохранить
  planning_candidates:   # READY_NOW + EXPECTED + dated regressions
  background_queue:      # BLOCKED / UNLINKED / старый хвост
  orphan_risks:
  regressions:
  packages:
  policies:              # из config, не применяются
missing_estimates:       # только work_item
feature_context:         # + work_stages, planning_constraints
planning_input:          # компактный вход для Phase 2
warnings:
```

`planning_input`: sprint, team, capacity, policies, candidates, context.post_work, work_items, constraints, qa, warnings.

`work_items` — уникальный identity: `primary_pool` + `appears_in` + `consumes_capacity`. Категории могут пересекаться, capacity считается один раз.

`candidates.carry_over` — только work items, которым ещё может понадобиться capacity следующего спринта.
`context.post_work` — To Prod / Delivery / To Test|Testing на dev-задачах. Raw `carry_over` на верхнем уровне не трогаем.

Каждая сущность, которую потом увидит человек, имеет `key` + `title` + `url`.

## planning_role

Configurable в `planning.yaml` → `planning_roles`:

- `work_item` — занимает capacity (Analysis, Development*, Bug/sBug, Testing, …)
- `container` — Epic, DeliveryStory, DiscoveryStory, Story
- `context_only` — Release и служебное

## feature vs epic

`feature.key` — DeliveryStory/DiscoveryStory. Никогда не подменяется Epic «потому что больше нечего».
Порядок: direct parent → Main/Sub task links → ancestor chain → notes schedule map (только если ключ сам story) → unresolved.

## JQL / источники Jira

Собираются в `sources.jql` каждого прогона. Типовые:

| Имя | Зачем |
|-----|--------|
| Agile `sprint/{id}/issue` | текущий спринт; named Ready for Dev / Ready to SA |
| `ready_for_development` | `project = CAT2 AND issuetype in (DevelopmentB, DevelopmentF, Bug) AND status in ("New") AND sprint is EMPTY` |
| `planning_period_keys` | `key in (CAT2-…)` из `schedule` активного `planning_periods` |
| `analysis_candidate_label` | `labels = <period.candidate_label>` |
| `backlog_changes` | created за lookback_days |
| `qa_queue_testing` | открытые `issuetype = Testing` |
| `qa_queue_old_flow` | `status = "To Test" AND labels = old-test-flow` |
| `dev_to_test` | dev в `To Test` |

Паттерны имён спринтов — в `planning.yaml` (`Ready for Development`, `Ready to SA`).

## Lane

Порядок сигналов: title prefix `[WEB]` / `[Back]` / … → component → platform → issue type.

`DevelopmentB` → `backend`. `DevelopmentF` **без** prefix/component/platform → `unknown_lane` (не считать web). Конфликт сигналов → `unknown_lane`.

## test ↔ dev links

Тип связи **не захардкожен**. Берутся все issue links, кроме `Testing`/`Epic`/`Sub-task`. Если в данных есть preferred types из config (`Relates`, `relates to`, …) — они приоритетны. Фактически встреченные типы пишутся в `qa.link_types_seen`.

Dev готова к тесту, если status ∈ `To Test`.

## ORPHAN_RISK

Ставится, если связанная (или old-flow) dev уже `To Test`, и при этом testing:

* не в текущем и не в следующем спринте, **или**
* без assignee, **или**
* в статусе lost-risk (`New` / `To Discovery` / `Discovery`).

Может сочетаться с `READY_NOW`.

## Holidays / time off

Окно = даты **планируемого** спринта (следующий после текущего). Weekdays минус `holidays` из schedule активного planning period минус `people[].time_off`. Формальные даты спринта не двигаются. Developer capacity: `developer_productive_hours_per_sprint` (60) × `person_working_days / typical_working_days`. Только developer lanes. SA/QA → `capacity_unknown`. Не использовать формулу `8h/day − meeting overhead`.

## Notes

Читаются, не переписываются:

* schedule активного `planning_periods` — priority, depends_on, bars, holidays, people; membership без priority тоже кандидат
* `features/all-features-list.md` — таблица: статус, бизнес-срок, релизы
* `features/items/**` — только явные маркеры (`не трогать`, `paused`, `ASAP`, `ждём`) и bullets секций «Решения» / «Открытые договорённости»
* `teams/*/README.md` — Jira username, QA role → capabilities
* `jira/testing-queue-notes.md` — явные пакеты (`### Пакет …`)

Свободный текст не интерпретируется. Неструктурированное кладётся как `context_notes` со `source`.

## QA history

`analyze_qa_history.py` пишет csv/json/md в `jira/reports/qa-history/`. В snapshot **не** подмешивается. Нормативы автоматически не выводятся.

Workflow задач типа Testing: **New → In Progress → Done**. Статус `Testing` — колонка разработки, не QA-задачи. Time in progress считается по `In Progress` / `В работе`.

## Lane vs work role (Phase 2)

Phase 1.5 `lane` — технический сигнал (prefix/component/type). Для Testing [Back] это `backend`.

Phase 2 разделяет:

- `work_role` — кто выполняет работу: `development` / `qa` / `sa` / `business_analysis` / `analysis_unknown`
- `planning_lane` — чью ёмкость занимает (`prepared_input.lane` = это поле)
- `source_lane` — исходный lane Phase 1.5
- `qa.tested_lane` — что тестируется; не ёмкость разработчика
- `analysis.kind` — `system` / `business` / `unknown` (не LLM)

Правила анализа из `planning.yaml` → `analysis_classification`:
`Specification` и `[SA]` → системный анализ; `[BA]` → бизнес-анализ; обычный Analysis без маркировки → неизвестный вид.

Testing всегда `work_role=qa`, `planning_lane=test`. Обычный Testing не фиксируется на Насте: eligible Настя+Костя, preferred Настя. PLP/PDP regression owner — по policy.

Phase 3 должна использовать `planning_lane` / `work_role`, не `source_lane`.

## Phase 2

Читает `planning_input`. Сырой snapshot — только provenance (`share` команды, `feature_context.work_stages`).

Статусы проверки: `READY` / `READY_WITH_WARNINGS` / `NEEDS_INPUT` / `INVALID_INPUT`.

`NEEDS_INPUT` ≠ «планировать нельзя». Это вопросы, которые желательно закрыть до Phase 3.

BLOCKER редко: нет окна спринта, нет команды, противоречащие authoritative constraints, обязательная задача без направления и без доступного исполнителя.

Не blocker: нет feature у бага, нет estimate у кандидата, unknown optional field, SA/QA capacity unknown, UNLINKED у регресса, `Нет жёсткого дедлайна`.

Гигиена: confirmed baseline = fact; unconfirmed recommendation = attention. Phase 2 не удаляет кандидатов по hygiene.

Выход: `jira/reports/preplanning/{date}__{project}__{plan-start}__validation.yaml` (+ `.md`).

## Phase 3

Читает `prepared_input` из отчёта Phase 2. Не дублирует модели Phase 2. Не пишет Jira.

Модули: `jira/scripts/planning/phase3/`. CLI: `jira/plan_sprint.py`. Сессии: `jira/reports/planning-sessions/`.

Статусы сессии: `COLLECTING_DECISIONS` / `DRAFT_READY` / `EDITING` / `READY_FOR_PREVIEW` / `PREVIEW_READY`.

Детерминированно: capacity, дубли, availability, eligibility, QA-окна, totals, diff, preview.  
LLM: формулировки, правки обычным языком, неоднозначные предпочтения.

Один issue — один раз. Post-work не занимает capacity. Testing — QA, не developers. SA — count/sequence, не выдуманные часы. Максим на Android только после явного решения.

## Phase 3 — feature-level planning

Единица продуктового планирования — Story-фича (`DeliveryStory` / `DiscoveryStory` / `Story`).

Семантика `feature_plan`:

- `candidate` — фичу имеет смысл рассмотреть; это ещё не план
- `known_work` — уже известные analysis/backend/web/admin/ios/android/testing issues
- `possible_next_sprint_work` — этапы, которые реально можно взять сейчас
- `unresolved` — unfinished SA, missing task, unknown next stage
- `planned_work` / `planned` — считается **после** выбора work items: `planned = planned_work is not empty`

Этапы в одном спринте могут быть analysis-only, development-only, testing-only или mix. Жёсткой машины `Analysis Done → только потом Development` нет.

Источники состава: explicit user decision → feature notes → Story / linked docs → linked Jira issues → inference только как assumption. Linked tasks ≠ полное описание фичи.

Active planning period приходит из `planning.yaml` → `planning_periods`. Collectors читают `period.schedule` и `period.candidate_label`. Generic Python не знает строку Q4. Если спринт **пересекает** начало следующего period, его candidates нужно рассматривать (для 21.09–02.10 это Q4 с 01.10). Если sprint полностью вне period — `stale_planning_period`. Если в period почти не осталось незавершённых кандидатов — warning, не blocker. Regression obligations при этом продолжают работать.

Регулярный регресс — `regression_obligations` в config, не наличие Testing issue. Нет Jira-задачи у required регресса → placeholder `needs_task=true`, слот QA занят, warning в draft, без вопроса и без удержания `COLLECTING_DECISIONS`. Optional commitment можно спросить, только если участие команды на период не подтверждено. Mobile dates только из Confluence, без odd/even week.

QA feature testing группируется в пакеты (`prefer_single_run`). Не использовать модель `1 Testing issue = 1 день`. Chanel / логобар — один пакет.

Confirmed user decisions хранятся как `facts` и не пересчитываются эвристикой при пересборке draft. Jira write запрещён, пока нет явного подтверждения apply.

Ready to Development остаётся отдельным источником после feature work. Обычный unrelated R2D не вытесняет выбранную фичу только из-за часов. Automatic backfill не считает человека полностью свободным при uncertain feature workload.

Задачи без оценки по нужной работе фичи остаются в consideration, чтобы появился вопрос об оценке. `sa_primary_count` не ограничивает feature-driven SA.


