FROM python:alpine3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]