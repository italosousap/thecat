FROM python:3.8-alpine
WORKDIR /app
ADD . /app
RUN apk update && pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]