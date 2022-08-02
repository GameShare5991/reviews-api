FROM python:3

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

WORKDIR /app

COPY requirements.txt /app/requirements.txt
# COPY serviceAccountKey.json /app/serviceAccountKey.json # If you want test in docker you can add this but do not share the image
RUN pip install -r requirements.txt --src /usr/local/src

COPY . .

EXPOSE 4005
CMD ["python", "reviewapi.py"]