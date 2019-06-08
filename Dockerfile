FROM python:3

WORKDIR /home/haha

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "manage.py runserver 0:8000"]