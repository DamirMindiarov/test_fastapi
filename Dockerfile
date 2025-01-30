FROM python:3.12-alpine

WORKDIR /test_fastapi

COPY /.github /test_fastapi/.github/
COPY /app /test_fastapi/app/
COPY /tests /test_fastapi/tests/
COPY /requirements.txt /test_fastapi/

RUN pip install -r /test_fastapi/requirements.txt
#ENTRYPOINT ["uvicorn"]
#
CMD ["uvicorn", "app.routes:app", "--host", "0.0.0.0"]
