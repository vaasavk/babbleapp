FROM python:alpine3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
<<<<<<< HEAD
CMD ["flask", "run", "--host=0.0.0.0"]
=======
CMD ["flask", "run", "--host=0.0.0.0"]
>>>>>>> d0068396c8684bc37e3cb25d9a18d706c96a3e22
