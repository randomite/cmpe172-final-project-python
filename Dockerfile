FROM python:3
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /src
EXPOSE 5000
CMD python run.py
