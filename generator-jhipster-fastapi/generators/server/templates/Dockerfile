FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN python3 -m venv venv
RUN source venv/bin/activate

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . . 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE <%= serverPort %>

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "<%= serverPort %>"]
