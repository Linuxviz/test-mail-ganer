_Python 2.7, django 1.11, celery, postgres_

Весь проект обернут в контейнеры, разворачивается просто docker-compose up. Для простоты развертки я включал .env файл в gitignore. 

Небольшой сервис по отправке писем. Пользователь имеет возможность загрузить несколько подписчиков за раз используя файл (сейчас реализован только json формат). Либо добавить одного вручную. Все подписчики принадлежат какой-либо группе. Подписчики загруженные из файла автоматически принадлежат одной группе. 

Шаблон письма загружается html файлом. В html файле можно использовать контекстные переменные {{name}}, {{second_name}}, {{birthday}}. Если переменные не найдены в данных подписчика, они будут пропущенный. В шаблоне не должно содержаться последовательности символов "{%" и "%}" иначе шаблон будет помечен как не валидный и удален с сервера. 

На странице отправки письма можно выбрать шаблон и группу которой он будет отправлен. Бэкенд сервер писем не подключен и письма отправляются в терминал. Сервер вставляет отслеживающий пиксель, который позволяет узнать сколько раз открывалось письмо и дату первого открытия.

main - приложение содержит логику связанную с пользователем

mailer - приложение содержащее основную логику формирования и отправки писем

core - приложение с настройками проекта