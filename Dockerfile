FROM python:3.9-slim

ARG TOKEN

WORKDIR /server

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update 
RUN apt-get install libgomp1
RUN apt-get install -y curl

RUN curl -H "Accept: application/vnd.github.v3.raw" -H "Authorization: token ${TOKEN}" -L https://api.github.com/Geode-solutions/open-license-manager/master/projects/geode/geode.lic
        

ENV GEODE_LICENSE_LOCATION=/server/geode.lic

CMD ["python3", "app.py"]

EXPOSE 5000

