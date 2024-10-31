## 📚 Документация API
[Документация API](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

## ✅ Выполнено:
- Практически все основные функции реализованы.

## 🚧 В планах:
- Написать несколько endpoint'ов API для функций удаления разрешения у пользователя, а также для прекращения отслеживания задачи.
- Связать уведомления с Telegram.

## 🚀 Как запустить проект?
1. Склонируйте репозиторий:  
   `git clone (https://github.com/AlanZhuman/tasktracker-test-project.git)`
   
2. Перейдите в корневую папку проекта (не в main/main, просто в ./, где находится файл docker-compose.yml):  
   
3. Заполните файл `.env.dev` своими данными. Пример можно найти в файле `.env_example` (ВАЖНО: не используйте файл .env, создайте .env.dev или измените имя .env в docker-compose.yml).
   
4. Введите в терминале:  
   `$ docker-compose up --build`
   
5. Подождите, пока приложения запустятся.

6. Откройте в браузере:  
   [http://127.0.0.1:8000/api/schema/swagger-ui/#/](http://127.0.0.1:8000/api/schema/swagger-ui/#/) или [http://0.0.0.0:8000/api/schema/swagger-ui/#/](http://0.0.0.0:8000/api/schema/swagger-ui/#/)

---

## 📚 API Documentation
[API Documentation](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

## ✅ Done:
- Almost all core functions implemented.

## 🚧 TODO:
- Write some API endpoints for functions.
- Link notifications with Telegram.

## 🚀 How to Start the Project?
1. Clone the repository:  
   `git clone (https://github.com/AlanZhuman/tasktracker-test-project.git)`
   
2. Navigate to the main project folder (not in main/main, just in ./ where docker-compose.yml is located):  
   
3. Fill up the `.env.dev` file with your own data. An example can be found in the `.env_example` file (IMPORTANT: DO NOT use the .env file; create .env.dev or change the .env filename in docker-compose.yml).
   
4. Type in the terminal:  
   `$ docker-compose up --build`
   
5. Wait for applications to startup.

6. Open in your browser:  
   [http://127.0.0.1:8000/api/schema/swagger-ui/#/](http://127.0.0.1:8000/api/schema/swagger-ui/#/) or [http://0.0.0.0:8000/api/schema/swagger-ui/#/](http://0.0.0.0:8000/api/schema/swagger-ui/#/)
