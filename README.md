# python-flask
 python 3 + flask + mysql 
**Create image for app python = Flask Mysql**

Tạo một file ứng ứng dụng bằng python3

[flask + Mysql: Quản lý sinh viên](https://www.notion.so/flask-Mysql-Qu-n-l-sinh-vi-n-755d976c15c644868a81235cc3951e07?pvs=21)

Tạo Docker file để chạy ứng dụng:

```bash
# vi Dockerfile
FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
CMD python app.py
```

File các gói yêu cầu:

```bash
#vi requirements.txt
Flask==2.0.1
mysql-connector==2.2.9
```

tạo file docker compose

```bash
# vi docker-compose.yaml
services:
  db:
    # We use a mariadb image which supports both amd64 & arm64 architecture
    # image: mariadb:10.6.4-focal
    # If you really want to use MySQL, uncomment the following line
    image: mysql:8.0.36
    container_name: db
    # command: '--default-authentication-plugin=mysql_native_password'
    command: mysqld --default-authentication-plugin=mysql_native_password --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    # volumes:
    #   - db_data:/var/lib/mysql
    # restart: always
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=someflask
      - MYSQL_DATABASE=flask
      - MYSQL_USER=flask
      - MYSQL_PASSWORD=flask
      - MYSQL_ALLOW_EMPTY_PASSWORD=yes
    expose:
      - 3306
      - 33060
    # ports:
    #   - '3306:3306'
    volumes:
      - './docker/db/data:/var/lib/mysql'
      - './docker/db/my.cnf:/etc/mysql/conf.d/my.cnf'
      - './docker/db/sql:/docker-entrypoint-initdb.d'
    networks:
      - app-network
      # - backend
  flask:
    build: ./backend
    links:
      - db
    depends_on:
      - db
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - MYSQL_ROOT_PASSWORD=someflask
      - MYSQL_DATABASE=flask
      - MYSQL_USER=flask
      - MYSQL_PASSWORD=flask
    networks:
      - app-network
      # - backend

volumes:
  db_data:

networks:
  app-network:
    driver: bridge
    external: true
    attachable: true
# networks:
#   backend:
#     driver: overlay
#     ipam:
#       config:
#         - subnet: 192.168.18.0/24
#     attachable: true
```

Để sử dụng trên docker thực hiện như sau:

```bash
mkdir app-python && cd app-python
git clone https://github.com/huydv398/python-flask.git

cd app-python/
#root@Docker:~/app-python# ls
#python-flask

cd python-flask/
# root@Docker:~/app-python/python-flask# ls
#backend  docker  docker-compose.yaml  README.md

docker compose up -d

```

Kết quả:

```bash
....

   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.25.0.3:5000/ (Press CTRL+C to quit)
```

truy cập vào bằng IP của máy chủ Docker để test thử

```bash
http://(IP_docker_srv):5000/
```

[https://stackoverflow.com/questions/51895326/connection-and-cursor-inside-a-class-in-psycopg2](https://stackoverflow.com/questions/51895326/connection-and-cursor-inside-a-class-in-psycopg2)

[https://github.com/pratamawijaya/example-flask-mysql-docker/blob/main/app/app.py](https://github.com/pratamawijaya/example-flask-mysql-docker/blob/main/app/app.py)

[https://www.devopsroles.com/deploy-flask-mysql-app-with-docker-compose/](https://www.devopsroles.com/deploy-flask-mysql-app-with-docker-compose/)