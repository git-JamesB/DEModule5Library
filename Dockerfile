FROM python:3.12.3
WORKDIR /app
COPY . /app
ENTRYPOINT [ "python", "data_cleaner.py" ]

RUN pip install -r requirements.txt
