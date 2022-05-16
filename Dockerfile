FROM python:3-bullseye

WORKDIR /usr/app/src

COPY . ./

RUN pip install -r ./requirements.txt
RUN git clone https://github.com/Rapptz/discord.py
RUN python3 -m pip install -U /usr/app/src/discord.py/.
CMD ["python", "./main.py"]