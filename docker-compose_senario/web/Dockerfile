FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "app.py" ]





#FROM python

#COPY . /app/
#WORKDIR /app/
#RUN pip3 install -r /app/requirements.txt
#EXPOSE 5000
#RUN pip install -r requirements.txt
#CMD ["python", "app.py"]
