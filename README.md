# Team lead skills

Скиллы тимлида для Cursor и ZCode: люди, встречи и план квартала. Карточки команды и личные заметки сюда не входят — скиллы пишут их в локальный workspace `notes/`.

Ревью системной аналитики — соседний репозиторий: https://github.com/kamisa1999-chipmunk/sa-skills

Jira, спринты и очередь теста — https://github.com/kamisa1999-chipmunk/jira-write

https://github.com/kamisa1999-chipmunk/teamlead-skills

## Скиллы

Каждый скилл — папка с `SKILL.md`. Подключение в Cursor — симлинк в `~/.cursor/skills/`.

| Папка | Зачем |
|-------|--------|
| `skills/1-1` | зафиксировать итоги 1:1, разобрать прошедшую встречу, подготовиться к следующей |
| `skills/meeting-context` | собрать с групповых встреч, что человек говорил, с таймкодами |
| `skills/observations` | записать наблюдение для обратной связи: факт отдельно от оценки |
| `skills/action-items` | личные обязательства тимлида и темы к кластер-лиду |
| `skills/quarter-gantt` | очередь квартала и Гант по ёмкости команды |

```bash
git clone https://github.com/kamisa1999-chipmunk/teamlead-skills.git
cd teamlead-skills
mkdir -p ~/.cursor/skills
for skill in 1-1 meeting-context observations action-items quarter-gantt; do
  ln -sfn "$(pwd)/skills/$skill" ~/.cursor/skills/$skill
done
```

Перезапусти Cursor или открой новый Agent chat. Если открыть этот репозиторий как workspace, скиллы подхватятся из `.cursor/skills/`.

Примеры фраз:

```text
зафиксируй 1:1
подготовься к 1:1 с Димой
обнови контекст по команде
зафиксируй наблюдение
мои action items
построй гант квартала
```

## Куда пишут

Скиллы дописывают локальные заметки, не этот репозиторий:

| Что | Куда |
|-----|------|
| карточка и история 1:1 | `notes/teams/{гильдия}/{slug}/` |
| контекст групповых встреч | `{slug}/meeting-context.md` |
| наблюдения | `{slug}/observations.md` |
| обязательства тимлида | `notes/leadership/kamilla-saidova.md` |
| прогон Ганта | `notes/features/gantt-runs/` |

Конспекты встреч скилл `meeting-context` ищет в `~/Downloads/` (`YYYY-MM-DD HHMM (MSK) {id}.txt`). Человека ищет по полю «Имя» в `notes/teams/{гильдия}/*/README.md`. Состав команды в скилл не зашит списком для Ганта: `quarter-gantt` читает те же карточки.

Факты из Jira к подготовке 1:1 — скилл `jira-employee-analysis` из [`jira-write`](https://github.com/kamisa1999-chipmunk/jira-write), и только после подтверждения.

## Установка в ZCode

Репозиторий упакован как ZCode-плагин (`.zcode-plugin/plugin.json` + `marketplace.json`).

1. Settings → Plugin Management → вкладка Discover → **`+`** → добавить `https://github.com/kamisa1999-chipmunk/teamlead-skills` как marketplace.
2. На карточке плагина `teamlead-skills` нажать **Get**. Скиллы появятся как `teamlead-skills:<имя-скилла>`.

Симлинками:

```bash
mkdir -p ~/.zcode/skills
for skill in 1-1 meeting-context observations action-items quarter-gantt; do
  ln -sfn "$(pwd)/skills/$skill" ~/.zcode/skills/$skill
done
```

Скиллы подхватятся в новой сессии ZCode.
