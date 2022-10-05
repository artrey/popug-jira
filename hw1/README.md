# HW1. Проектирование

## [Постановка задачи](https://lms.tough-dev.school/materials/33cbbaacdee545f89cfe4204af973bd9/)

---

## ES схема ([вся схема в Miro](https://miro.com/app/board/uXjVPR8jkNs=/?share_link_id=866292287349))

- ## Auth system

![Auth system](<../assets/v2/Awesome%20Task%20Exchange%20System%20(aTES)%20v2%20-%20Auth%20system.jpg>)

- ## Task system

![Task system](<../assets/v2/Awesome%20Task%20Exchange%20System%20(aTES)%20v2%20-%20Task%20system.jpg>)

- ## Accounting system

![Accounting system](<../assets/v2/Awesome%20Task%20Exchange%20System%20(aTES)%20v2%20-%20Accounting.jpg>)

- ## Analytics system

![Analytics system](<../assets/v2/Awesome%20Task%20Exchange%20System%20(aTES)%20v2%20-%20Analytics.jpg>)

---

## Data/Domain model ([вся схема в Miro](https://miro.com/app/board/uXjVPR8jkNs=/?share_link_id=866292287349))

![Data model](<../assets/v2/Awesome%20Task%20Exchange%20System%20(aTES)%20v2%20-%20Data%20Model.jpg>)

---

## Схема сервисов ([вся схема в Miro](https://miro.com/app/board/uXjVPR8jkNs=/?share_link_id=866292287349))

![Схема сервисов](<../assets/v2/Awesome%20Task%20Exchange%20System%20(aTES)%20v2%20-%20Services.jpg>)

---

## События в системе

### Бизнес события

- Task service:

- - Задача создана [id, попуг-создатель.id, попуг-исполнитель.id]. Потребители: Accounting service | Analytics service
- - Задача заассайнена [какая задача и на кого (попуг)]. Потребители: Accounting service
- - Задача выполнена [какая задача и кем (попуг)]. Потребители: Accounting service
- - Затребован реассайн задач (возможно полезно для аналитики будет) [кто затребовал (попуг)]. Потребители: Accounting service | Analytics service

---

- Accounting service:

- - Деньги зачислены [кому (аккаунт), причина (какая задача), сколько]. Потребители: Analytics service
- - Деньги списаны [у кого (аккаунт), причина (какая задача), сколько]. Потребители: Analytics service
- - Вывод денег инициирован (возможно полезно для отладки будет, если с платежным шлюзом проблемы будут) [для кого (аккаунт), сколько, timestamp]. Потребители: Analytics service (?)
- - Вывод денег произведен [для кого (аккаунт), сколько, timestamp]. Потребители: Analytics service

### CUD события

- Auth service:

- - Попуг создан/изменен/удален [id, роль и ФИО]. Потребители: Task service | Accounting service | Analytics service

---

- Accounting service:

- - Обновлена задача [стоимость ассайна, вознаграждение за выполнение]. Потребители: Analytics service
- - Аккаунт создан [id, попуг.id]. Потребители: Analytics service
- - Аудит-лог создан [id, аккаунт.id, тип, сумма, причина (задача.id)]. Потребители: Analytics service
