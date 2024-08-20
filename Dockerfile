FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the application code
COPY . /app

WORKDIR /app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8083"]
