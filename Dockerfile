FROM python:3.9-slim-buster 

WORKDIR /server

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

# pour installer libgomp - sinon problème d'importation louche
RUN apt-get update 
RUN apt-get install libgomp1

CMD ["python3", "app.py"]

EXPOSE 5000