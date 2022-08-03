FROM python:3.9.2-alpine
RUN mkdir /usr/src/devman_notifications_bot_docker
WORKDIR /usr/src/devman_notifications_bot_docker
COPY requirements.txt /usr/src/devman_notifications_bot_docker
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "get_devman_notifications.py"]