FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update
RUN apt-get update && apt-get install -y python3-opencv
RUN python3 -m pip install --upgrade pip
COPY ./ /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app:app", "--reload", "--workers", "2","--host","0.0.0.0", "--port","8000"]
