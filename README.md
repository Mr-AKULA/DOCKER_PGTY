### README.md

```markdown
# DOCKER_PGTY

## Описание

Этот проект представляет собой веб-приложение на Flask, которое извлекает данные из базы данных InfluxDB и визуализирует их с помощью Plotly. Приложение использует Docker для контейнеризации, что облегчает его развертывание и управление.

## Основные функции

- Извлечение данных из InfluxDB.
- Визуализация данных с помощью Plotly.
- Отображение графиков на веб-странице.
- Контейнеризация с помощью Docker.

## Установка и запуск

### Предварительные условия

- Установлен Docker.
- Установлен Docker Compose.

### Шаги

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/Mr-AKULA/DOCKER_PGTY.git
    cd DOCKER_PGTY
    ```

2. **Создайте и запустите контейнеры:**

    ```bash
    docker-compose up --build
    ```

3. **Откройте веб-браузер и перейдите по адресу:**

    ```
    http://localhost:5000
    ```

## Структура проекта

- **app.py**: Основной файл Flask-приложения.
- **templates/**: Шаблоны HTML для отображения веб-страниц.
- **Dockerfile**: Файл для создания Docker-образа.
- **docker-compose.yml**: Файл для определения и запуска многоконтейнерных Docker-приложений.
- **requirements.txt**: Файл с зависимостями проекта.

## Использование

1. **Извлечение данных из InfluxDB**:
    - Приложение извлекает данные из InfluxDB с использованием Flux-запросов.
    - Данные фильтруются и преобразуются в DataFrame с помощью Pandas.

2. **Визуализация данных**:
    - Данные визуализируются с помощью Plotly.
    - Графики отображаются на веб-странице.

3. **Отображение графиков**:
    - Веб-страница отображает временные ряды данных и метрики.
    - Графики обновляются в реальном времени.

## Пример данных

Пример данных, которые могут быть использованы для тестирования:

```plaintext
# sensors_data_prediction
_time                           _value  _field  _measurement  mae    r2  SensorID DataType
------------------------------  ------  ------- ------------- ---- ---- --------- --------
2024-04-18T00:01:35Z           40.826  sgd     sensors_data  36.8  -0.166736 10        prediction
2024-04-18T00:01:36Z           47.629  sgd     sensors_data  36.8  -0.166736 10        prediction
2024-04-18T00:01:37Z           43.303  sgd     sensors_data  36.8  -0.166736 10        prediction
```

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь с автором проекта:

- GitHub: [Mr-AKULA](https://github.com/Mr-AKULA)

## Благодарности

Спасибо всем, кто внес вклад в этот проект!
```

### Дополнительные шаги

1. **Создайте файл `LICENSE`**:
    - Добавьте файл `LICENSE` в корневой каталог вашего репозитория и вставьте в него текст лицензии MIT.

2. **Добавьте файл `.gitignore`**:
    - Создайте файл `.gitignore` в корневом каталоге вашего репозитория и добавьте в него следующие строки:

    ```plaintext
    __pycache__/
    *.pyc
    .env
    ```

3. **Обновите файл `requirements.txt`**:
    - Убедитесь, что файл `requirements.txt` содержит все необходимые зависимости:

    ```plaintext
    Flask==2.0.2
    pandas==1.3.3
    influxdb-client==1.17.0
    plotly==5.3.1
    ```

4. **Создайте файл `docker-compose.yml`**:
    - Добавьте файл `docker-compose.yml` в корневой каталог вашего репозитория и вставьте в него следующее содержимое:

    ```yaml
    version: '3.8'

    services:
      web:
        build: .
        ports:
          - "5000:5000"
        environment:
          - INFLUXDB_TOKEN=your_influxdb_token
          - INFLUXDB_URL=http://influxdb:8086
          - INFLUXDB_ORG=your_org
          - INFLUXDB_BUCKET=your_bucket
        depends_on:
          - influxdb

      influxdb:
        image: influxdb:latest
        ports:
          - "8086:8086"
        environment:
          - DOCKER_INFLUXDB_INIT_MODE=setup
          - DOCKER_INFLUXDB_INIT_USERNAME=your_username
          - DOCKER_INFLUXDB_INIT_PASSWORD=your_password
          - DOCKER_INFLUXDB_INIT_ORG=your_org
          - DOCKER_INFLUXDB_INIT_BUCKET=your_bucket
          - DOCKER_INFLUXDB_INIT_RETENTION=1w
          - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=your_influxdb_token
    ```

5. **Создайте файл `Dockerfile`**:
    - Добавьте файл `Dockerfile` в корневой каталог вашего репозитория и вставьте в него следующее содержимое:

    ```Dockerfile
    # Use the official Python image from the Docker Hub
    FROM python:3.9-slim

    # Set the working directory
    WORKDIR /app

    # Copy the requirements file into the container
    COPY requirements.txt .

    # Install the dependencies
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the rest of the application code into the container
    COPY . .

    # Expose the port the app runs on
    EXPOSE 5000

    # Run the application
    CMD ["python", "app.py"]
    ```
