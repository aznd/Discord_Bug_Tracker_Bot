FROM debian:10.9

LABEL version="1.0"
LABEL description="Docker image for the discord bug tracker"

CMD ["python", "main.py"]