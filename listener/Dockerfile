FROM python:3

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8081 

CMD ["python","-u", "listener.py"]


