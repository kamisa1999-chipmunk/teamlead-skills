# Образцы структуры

Вымышленный книжный сервис **BookShelf**. Имена, встречи, фичи и ключи `SHELF-` придуманы. Это форма файлов, не заметки команды.

Живые данные скиллы читают и пишут в workspace `notes/`: `teams/`, `features/`, `leadership/`. Сюда их не копировать.

| Что | Образец |
|-----|---------|
| Пустой каркас карточки | [teams/_template.md](teams/_template.md) |
| Заполненная карточка человека | [teams/web/alisa-voronova/](teams/web/alisa-voronova/README.md) |
| Конспект 1:1 | [transcripts/2026-06-18 1030 (MSK) 9001002001.txt](transcripts/2026-06-18%201030%20(MSK)%209001002001.txt) |
| Конспект групповой встречи | [transcripts/2026-06-25 1400 (MSK) 9001002002.txt](transcripts/2026-06-25%201400%20(MSK)%209001002002.txt) |
| Action items тимлида | [leadership/teamlead.md](leadership/teamlead.md) |
| Индекс фич | [features/all-features-list.md](features/all-features-list.md) |
| Папка фичи | [features/items/01-reading-list/](features/items/01-reading-list/01-reading-list.md) |
| Срез квартального плана | [features/q3-plan.md](features/q3-plan.md) |
| YAML для Ганта | [features/schedule.example.yaml](features/schedule.example.yaml) |

Текст Story и постановка SA-задачи лежат в папке фичи как `story-draft.md` и `sa-task-draft.md`. В работу они уходят в Jira через скилл `jira-write`, отдельным каноном фичи не становятся.
