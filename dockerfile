FROM python:3.8
WORKDIR /test-project
COPY * .
RUN pip install -r requirements.txt
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
VOLUME ["/work_test"]
EXPOSE 5000
ENV HOST 0.0.0.0
ENV DEBUG true
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--preload"]
