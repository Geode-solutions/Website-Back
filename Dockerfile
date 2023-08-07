FROM python:3.9-slim

WORKDIR /server

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update 
RUN apt-get install libgomp1

CMD ["python3", "app.py"]

EXPOSE 5000