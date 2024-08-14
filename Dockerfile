FROM python:3.10.0-slim
MAINTAINER AI
ENV TZ=Asia/Shanghai
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/home
WORKDIR $APP_HOME
ENV PYTHONPATH "${PYTHONPATH}:$APP_HOME"
COPY . $APP_HOME
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    pip install --no-cache-dir -r requirements.txt
