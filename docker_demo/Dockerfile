FROM python:3.12.3
WORKDIR /app
COPY . /app
ENTRYPOINT [ "python", "docker_calc.py" ]

RUN pip install pandas
RUN python times_table.py