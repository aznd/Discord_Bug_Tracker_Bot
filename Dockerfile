FROM python:3-bullseye

WORKDIR /usr/app/src

COPY . ./

RUN pip install -r ./requirements.txt
RUN python3 -m pip install https://github.com/Rapptz/discord.py
CMD ["python", "./main.py"]
