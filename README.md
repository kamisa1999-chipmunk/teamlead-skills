# Team lead skills

Скиллы тимлида для Cursor и ZCode: люди, встречи, вход в фичу, постановка задач и план квартала. Живые карточки и фичи сюда не входят — скиллы пишут их в workspace `notes/`. Форма файлов — в [examples/](examples/README.md), на вымышленном сервисе BookShelf.

Ревью системной аналитики — https://github.com/kamisa1999-chipmunk/sa-skills

Запись в Jira, спринтовый снимок, итоги и очередь теста — https://github.com/kamisa1999-chipmunk/jira-write

`story-prep` и `sa-task-prep` готовят текст задачи и после подтверждения передают его в `jira-write`. Сами в Jira не ходят.

https://github.com/kamisa1999-chipmunk/teamlead-skills

## Скиллы

Каждый скилл — папка с `SKILL.md`. Подключение в Cursor — симлинк в `~/.cursor/skills/`.

| Папка | Зачем |
|-------|--------|
| `skills/1-1` | зафиксировать итоги 1:1, разобрать прошедшую встречу, подготовиться к следующей |
| `skills/meeting-context` | собрать с групповых встреч, что человек говорил, с таймкодами |
| `skills/observations` | записать наблюдение для обратной связи: факт отдельно от оценки |
| `skills/action-items` | личные обязательства тимлида и темы к кластер-лиду |
| `skills/feature-assessment` | входной разбор сырого запроса: потребность, зона команды, грубая оценка |
| `skills/story-prep` | DeliveryStory до системного анализа; в Jira — через `jira-write` |
| `skills/sa-task-prep` | постановка задачи аналитику по готовой Story; в Jira — через `jira-write` |
| `skills/solution-research` | варианты решения и recommendation, без выбора архитектуры за команду |
| `skills/quarter-gantt` | очередь квартала и Гант по ёмкости команды |
| `skills/sprint-planning` | снимок, готовность и черновик следующего спринта |
| `skills/backlog-hygiene` | read-only аудит бэклога, без записи в Jira |

```bash
git clone https://github.com/kamisa1999-chipmunk/teamlead-skills.git
cd teamlead-skills
mkdir -p ~/.cursor/skills
for skill in 1-1 meeting-context observations action-items feature-assessment story-prep sa-task-prep solution-research quarter-gantt sprint-planning backlog-hygiene; do
  ln -sfn "$(pwd)/skills/$skill" ~/.cursor/skills/$skill
done
```

Перезапусти Cursor или открой новый Agent chat. Если открыть этот репозиторий как workspace, скиллы подхватятся из `.cursor/skills/`.

Примеры фраз:

```text
зафиксируй 1:1
подготовься к 1:1
обнови контекст по команде
зафиксируй наблюдение
мои action items
прикинь, как это сделать
подготовь story
подготовь SA-задачу
проработай техническое решение
построй гант квартала
подготовь следующий спринт
```

## Куда пишут

Скиллы дописывают локальные заметки, не этот репозиторий:

| Что | Куда |
|-----|------|
| карточка и история 1:1 | `notes/teams/{гильдия}/{slug}/` |
| контекст групповых встреч | `{slug}/meeting-context.md` |
| наблюдения | `{slug}/observations.md` |
| обязательства тимлида | `notes/leadership/kamilla-saidova.md` |
| папка фичи | `notes/features/items/<nn>-<slug>/` |
| прогон Ганта | `notes/features/gantt-runs/` |

Как это выглядит заполненным — [examples/](examples/README.md): карточка Алисы Вороновой, конспект, индекс фич и папка «список чтения». Персонажи выдуманы.

Конспекты встреч скилл `meeting-context` ищет в `~/Downloads/` (`YYYY-MM-DD HHMM (MSK) {id}.txt`). Человека ищет по полю «Имя» в `notes/teams/{гильдия}/*/README.md`. Состав команды в скилл не зашит списком для Ганта: `quarter-gantt` читает те же карточки.

Факты из Jira к подготовке 1:1 — скилл `jira-employee-analysis` из [`jira-write`](https://github.com/kamisa1999-chipmunk/jira-write), и только после подтверждения.

## Установка в ZCode

Репозиторий упакован как ZCode-плагин (`.zcode-plugin/plugin.json` + `marketplace.json`).

1. Settings → Plugin Management → вкладка Discover → **`+`** → добавить `https://github.com/kamisa1999-chipmunk/teamlead-skills` как marketplace.
2. На карточке плагина `teamlead-skills` нажать **Get**. Скиллы появятся как `teamlead-skills:<имя-скилла>`.

Симлинками:

```bash
mkdir -p ~/.zcode/skills
for skill in 1-1 meeting-context observations action-items feature-assessment story-prep sa-task-prep solution-research quarter-gantt sprint-planning backlog-hygiene; do
  ln -sfn "$(pwd)/skills/$skill" ~/.zcode/skills/$skill
done
```

Скиллы подхватятся в новой сессии ZCode.
