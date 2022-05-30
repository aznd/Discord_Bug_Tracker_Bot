FROM python:3-bullseye

WORKDIR /usr/app/src

COPY . ./

RUN pip install -r ./requirements.txt
CMD ["python", "./main.py"]
