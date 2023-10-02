FROM node:lts-alpine3.18 as dist


    RUN mkdir frontend
    WORKDIR /frontend

    # копируем оба 'package.json' и 'package-lock.json'
    COPY /frontend/package*.json ./


    # устанавливаем зависимости проекта
    RUN npm install

    # Копируем файлы проекта
    COPY /frontend /frontend

    # Копируем файл .env.production из родительского каталога в /frontend
    COPY .env.production ./

    # Собираем фронтенд при помощи Vite
    RUN npm run build

# Создаем образ Nginx для развертывания фронтенда
FROM nginx:alpine
    # Копируем собранные файлы из билдера в контейнер Nginx
    COPY --from=dist /frontend/dist /usr/share/nginx/html
    # Копируем конфигурацию
    COPY /frontend/nginx.conf /etc/nginx/nginx.conf
    # Требуется порт 80 для Nginx
    EXPOSE 80