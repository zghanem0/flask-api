FROM python

COPY . /app/
WORKDIR /app/
RUN pip3 install -r /app/requirements.txt
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
