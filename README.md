## 📚 Документация API
[Документация API](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

## ✅ Выполнено:
- Все основные функции кроме отправки уведомлений через телеграм реализованы.

## 🚧 В планах:
- Связать уведомления с Telegram.
- Переписать несколько эндпонтов для более удобного взаимодействия.

## 🚀 Как запустить проект?
1. Склонируйте репозиторий:  
   `git clone https://github.com/AlanZhuman/tasktracker-test-project.git`
   
2. Перейдите в корневую папку проекта (не в main/main, просто в ./, где находится файл docker-compose.yml):  
   
3. Заполните файл `.env.dev` своими данными. Пример можно найти в файле `.env_example` (ВАЖНО: не используйте файл .env, создайте .env.dev или измените имя .env в docker-compose.yml).
   
4. Введите в терминале:  
   `$ docker-compose up --build`
   
5. Подождите, пока приложения запустятся.

6. Откройте в браузере:  
   [http://127.0.0.1:8000/api/schema/swagger-ui/#/](http://127.0.0.1:8000/api/schema/swagger-ui/#/) или [http://0.0.0.0:8000/api/schema/swagger-ui/#/](http://0.0.0.0:8000/api/schema/swagger-ui/#/)

7. ВАЖНО: Возможно после запуска будет необходимость в следующих действиях:
   1. Зайти в Django сервис через консоль при помощи команды `$ docker exec -i -t django /bin/bash`
   2. Создать суперпользователя
   3. Авторизоваться в Django Admin
   4. Создать группы доступа со следующими названиями: `"CRUD-user", "R-User", 'Pm-user"`


---

## 📚 API Documentation
[API Documentation](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

## ✅ Done:
- All core functions, except telegram notifications implemented.

## 🚧 TODO:
- Link notifications with Telegram.
- Rewrite few endpoints for better interaction with them.

## 🚀 How to Start the Project?
1. Clone the repository:  
   `git clone https://github.com/AlanZhuman/tasktracker-test-project.git`
   
2. Navigate to the main project folder (not in main/main, just in ./ where docker-compose.yml is located):  
   
3. Fill up the `.env.dev` file with your own data. An example can be found in the `.env_example` file (IMPORTANT: DO NOT use the .env file; create .env.dev or change the .env filename in docker-compose.yml).
   
4. Type in the terminal:  
   `$ docker-compose up --build`
   
5. Wait for applications to startup.

6. Open in your browser:  
   [http://127.0.0.1:8000/api/schema/swagger-ui/#/](http://127.0.0.1:8000/api/schema/swagger-ui/#/) or [http://0.0.0.0:8000/api/schema/swagger-ui/#/](http://0.0.0.0:8000/api/schema/swagger-ui/#/)

7. IMPORTANT: The following actions may be necessary after startup:
   1. Enter Django service through the console with `$ docker exec -i -t django /bin/bash`
   2. Create a superuser
   3. Authorize in Django Admin
   4. Create access groups with the following names: 'CRUD-user', 'R-User', 'Pm-user'