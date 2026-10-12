# Backlog hygiene — правила фактов и рекомендаций

Скрипты детерминированы. LLM не обходит Jira повторно за фактами из YAML.

## Planning role (из `hygiene.yaml`)

| role | смысл |
|------|--------|
| `work_item` | Реальная работа, занимает capacity |
| `container` | Группировка (Epic, DeliveryStory, DiscoveryStory, Story) |
| `context_only` | Не работа команды (Release, Sub-task, неизвестный тип) |

Epic **не** считать фичей автоматически. `feature` — DeliveryStory/DiscoveryStory.

## Сигналы

Негативные: `container_in_sprint`, `container_repeated_in_sprints`, `stale_no_activity`, `very_old_new_issue`, `no_assignee`, `no_feature`, `no_parent`, `all_children_closed`, `no_active_children`, `closed_children_but_open_container`, `repeated_sprint_carry`, `carry_without_recent_activity`, `old_testing_tail`, `orphan_testing`, `testing_without_dev`, `dev_ready_but_testing_not_planned`, `ready_dev_without_feature`, `ready_dev_without_assignee`, `ready_dev_without_estimate`, `duplicate_candidate`, `superseded_candidate`, `not_in_notes`, `needs_product_decision`.

Защитные: `recent_activity`, `active_children`, `has_deadline`, `has_release_constraint`, `still_in_notes`, `quarter_candidate`, `active_dependency`, `external_dependency`, `explicit_keep_decision`.

`not_in_notes` — только сигнал. Дубли — только явные Jira-связи (`duplicates`, `clones`, `supersedes`, …).

## Рекомендации

| action | когда |
|--------|--------|
| `REMOVE_FROM_SPRINT` high | контейнер в текущем спринте |
| `CLOSE_CANDIDATE` medium | контейнер, все children закрыты, нет защитных notes/срока; или старый Testing-хвост |
| `NEEDS_OWNER` | потерянная Testing; ready-dev без assignee; To Test без Testing |
| `NEEDS_PRODUCT_DECISION` | зависшая идея, нужна ясность продукта |
| `MERGE_OR_SUPERSEDED` high | явная duplicate-связь |
| `INVESTIGATE` low/medium | слабые сигналы, возраст без защиты |
| `KEEP` | защитные сигналы или нет проблем |

`REMOVE_FROM_SPRINT` ≠ `CLOSE_CANDIDATE`. Возраст ≠ закрыть.

## Fingerprint / скрытие

Сравниваются: status, sprint_ids, assignee, child_counts, active_children, links, feature, deadline, fix_versions.

Скрывать в pre-sprint, если решение есть, fingerprint тот же, `review_after` ещё не наступил. **Не скрывать** контейнер в активном спринте, если `allow_in_sprint: false`.

## Пользовательский язык

В ответах только русский. Enum оставлять во внутреннем YAML.

- High-confidence cleanup → Можно уверенно почистить
- Needs human decision → Нужна ручная проверка
- Container pollution → Лишние контейнеры в спринтах
- Stale backlog → Залежавшиеся задачи
- Orphan testing → Потерянная задача тестирования
- Carry-over → Незавершённые задачи из прошлого спринта
- Baseline → История принятых решений
- Suppressed → Временно скрыто до следующей проверки

Статусы и типы Jira не переводить: `To Test`, `DeliveryStory`.

Ключи в Markdown: `[CAT2-123 — Название задачи](https://jira01.goldapple.ru/browse/CAT2-123)`.
В ссылке всегда ключ и название, чтобы можно было решить, не открывая Jira.
