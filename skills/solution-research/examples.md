# Примеры Solution-research

Читать только если нужен образец формулировок. Не подставлять примеры в живой research как факты. Не оптимизировать разбор под живые CAT2 из обсуждения скилла.

## Команды

```text
проработай техническое решение по CAT2-XXXX
сделай solution research по этой фиче
сравни эти два варианта и посмотри код
как лучше реализовать эту фичу?
зафиксируй, что берём вариант B
```

## Маленький искусственный пример

Вход (выдуманная задача, не боевая фича):

```text
DEMO: на PLP показывать бейдж «Outlet» у товаров с признаком outlet.
Пользователь предлагает отдельный Outlet API.
```

Внутренне: потребность отдельно; отдельный Outlet API = `OPTION` / `USER_INPUT`, не `DECISION`.

Скелет на диске (обязателен, выдуманная DEMO-фича):

```text
notes/features/items/99-outlet-plp-badge/
  99-outlet-plp-badge.md
  solution-research.md
  current-state.puml
  target-state.puml
```

Живая заметка — цель, Jira, статус, пустая таблица Decisions, блок «Recommendation (не решение)». Research — current state, comparison, evidence. Не копировать цель целиком в research.

Ниже — сжатый образец **содержимого research**, не шаблон под все фичи.

### Decision-ready summary

Нужно пометить outlet-товары на PLP. Сейчас у карточки товара уже есть набор бейджей из каталожного ответа; отдельного Outlet API в доступном коде не видно. Сравнивали: (A) отдельный API, (B) расширить текущий PLP-контракт флагом. Рекомендация — B. Риски: старые приложения проигнорируют неизвестное поле, если контракт это допускает; иначе нужен versioning. Ещё нужно решить: источник признака outlet и нужна ли админка.

### Current state

PLP-клиенты читают список бейджей из ответа каталога. Отдельного сервиса outlet skill не нашёл.

```text
web-catalog → src/plp/ProductBadges.ts → renderBadges()
catalog-bff → Plp/V2/ProductResponse → Badges
```

Это `FACT` по коду. Источник признака outlet в админке — `OPEN_QUESTION`.

### Impact map

- backend / BFF: likely — откуда взять признак и отдать его в PLP
- web / iOS / Android: likely — отрисовка бейджа
- contracts: likely
- admin: possible
- отдельный новый сервис: not relevant, если выбран Option B

### Options

**Option 1 — отдельный Outlet API.** `USER_INPUT`. Новый контракт и интеграция на всех клиентах. Старые приложения бейдж не получат, пока не обновятся. Высокая delivery complexity.

**Option 2 — флаг/бейдж в текущем PLP-ответе.** `INFERENCE` из существующего механизма бейджей. Один контур. Старые клиенты, скорее всего, игнорируют неизвестное поле — проверить контракт. Нужно подтвердить источник данных.

Новый Option 3 не добавлять: отдельный клиентский хардкод списка SKU не имеет технического основания в текущем каталоге.

### Comparison

| Критерий | Option 1. Отдельный API | Option 2. Флаг в PLP |
|---|---|---|
| Backend changes | новый сервис/ручка | расширение текущего ответа |
| Client changes | все клиенты, новый клиент | все клиенты, существующий badges renderer |
| Old clients | не увидят бейдж до обновления | вероятно без поломки, если поле optional |
| Coupling | новый контур | существующий PLP |
| Delivery complexity | высокая: контракт + все платформы + rollout | ниже: один контракт |
| Risks | дублирование модели товара | неверный источник признака |

### Recommended option

Option 2 — расширить текущий PLP-ответ.

Почему: уже есть механизм бейджей; меньше новых интеграций; ниже координация релизов.

Assumptions: признак outlet уже есть или появится в каталожном источнике PLP; клиенты умеют игнорировать неизвестные optional-поля.

Trade-off: не получаем отдельную эволюцию outlet-домена вне PLP.

Это `RECOMMENDATION`, не `DECISION`. В живой заметке — блок «Recommendation (не решение)», таблица Decisions пустая.

После «берём вариант 2» — строка в Decisions живой заметки. `target-state.puml` уже лежит в папке как схема рекомендации; после выбора поправить title, что контур принят.

### PlantUML
@startuml demo-outlet-current-state
title DEMO current state — бейджи PLP
actor User
participant "Web / iOS / Android" as FE
participant "Catalog BFF" as BFF

User -> FE: открыл PLP
FE -> BFF: PLP request
BFF --> FE: products + badges
FE -> User: карточки с бейджами
note right of BFF: отдельного Outlet API нет
@enduml
```

Для этой задачи sequence достаточно. C4 и state-диаграммы не нужны. Файлы всё равно класть в папку фичи: `current-state.puml` и `target-state.puml` (target — Option 2 как recommendation).

## Recommendation vs decision

| Формулировка | Метка |
| --- | --- |
| «Skill рекомендует фильтровать на BFF» | `RECOMMENDATION` |
| «Пользователь предлагает отдельный API» | `USER_INPUT` / `OPTION` |
| «В коде уже есть общий badges renderer» | `FACT` |
| «Похоже, админка не отдаёт этот признак» | `INFERENCE` |
| «Берём вариант 2, фиксируй» | `DECISION` |

Плохо: записать recommendation в «Decisions» до явного выбора.

Плохо: сохранить только `notes/features/items/99-outlet-plp-badge-research.md` без папки и живой заметки.
