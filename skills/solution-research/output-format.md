# Формат technical design package

Читать **перед первым пользовательским выводом и перед записью файлов**. Не читать в начале прогона.

Результат должен быть пригоден для design review. Внутренний чеклист pipeline и полную разметку provenance не показывать, если не просили технический отчёт.

Русские названия блоков. Id меток (`FACT`, `OPTION`, `DECISION`) оставлять как есть, если нужны для однозначности.

Не создавать пустые секции.

## Обязательный пакет

### 1. Decision-ready summary

Коротко, читается за 1–2 минуты:

- что меняем;
- current state;
- основные варианты;
- recommended option;
- ключевые риски;
- какие решения ещё нужны.

### 2. Current state

Техническая картина существующей системы. Evidence рядом с утверждениями.

### 3. Impact map

Что затрагивается. Только релевантное. `confirmed` / `likely` / `possible`.

### 4. Options & comparison

Исследованные варианты и компактное сравнение.

### 5. Recommendation

Рекомендуемый вариант и rationale. Явно: это `RECOMMENDATION`, не `DECISION`.

### 6. Open questions / assumptions

Что не подтверждено. Вопросы: `blocking` / `non-blocking`, 1–5 за итерацию.

### 7. Sources / evidence

Jira, Confluence, feature notes, repo paths, symbols.

## Диаграммы в скелете

`current-state.puml` и `target-state.puml` входят в обязательный скелет (см. `skeleton.md`). Target-state рисует recommended option и в title не выдаёт его за принятое решение.

## Прочие артефакты

Создавать только если они реально помогают, в ту же папку:

- `sequence.puml`;
- таблица contract changes;
- migration notes;
- rollout plan;
- список follow-up Jira tasks (не создавать задачи);
- draft ADR / technical decision record.

## Диаграммы

Формат по умолчанию — **PlantUML**.

Допустимы: component diagram; C4-PlantUML, если подходит существующему контексту; sequence; activity; state.

Не создавать диаграмму только ради наличия диаграммы. Если контура нет — файла может не быть, с объяснением в чате.

### Mermaid

Mermaid **не использовать автоматически**.

Если конкретный артефакт существенно лучше реализуется Mermaid — сначала объяснить преимущество и запросить явное подтверждение.

Без подтверждения — PlantUML или текстовый формат.

## Хранение

Читать `skeleton.md` и следовать ему. Краткая норма:

```text
notes/features/items/<nn>-<slug>/
  <nn>-<slug>.md
  solution-research.md
  current-state.puml
  target-state.puml
```

Не сохранять пакет россыпью в корне `items/`. Живая заметка обязательна. Recommendation — в research и в блок «Recommendation (не решение)» заметки, не в таблицу Decisions.

Существующую заметку не переписывать с нуля: ссылка, статус, recommendation. Diff в чат — только если правка ломает чужую структуру; обычное дополнение скелета показывать путями файлов.

## Шаблон файла

```markdown
# <Feature> — Solution Research

← [живая заметка](./<nn>-<slug>.md)
Jira: ...

## Decision-ready summary

## Problem / scope

## Confirmed current state

## Current-state architecture

## Impact map

## Options

### Option 1
...

### Option 2
...

## Comparison

## Recommended option

## Open questions

## Assumptions

## Decisions
Пока нет / confirmed decisions

## Evidence / sources
### Jira / Confluence
### Code
### Feature notes
```

Секции вроде Backward compatibility, Estimate, Target state, Follow-up — только если нужны.

## Показ пользователю

Сначала decision-ready summary в чате. Затем указать **папку** и файлы скелета.

Не спрашивать разрешения «создать ли feature note» — для этого скилла папка обязательна. Спрашивать, только если неясно, какая это фича / какой номер.

Следующий шаг предлагать, не запускать:

- зафиксировать `DECISION`, если пользователь выбирает вариант;
- `story-prep` / `sa-task-prep`, если нужна постановка;
- follow-up Jira — список, без создания карточек.
