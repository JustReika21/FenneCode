FROM python:3.12

WORKDIR /fennecode

COPY . /fennecode/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "fennecode.wsgi:application", "--bind", "0.0.0.0:8000"]
