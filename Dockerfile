FROM python:alpine3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
RUN apk add curl
HEALTHCHECK --interval=10s --timeout=10s CMD curl -f http://localhost:5000/api/blabs || exit 1