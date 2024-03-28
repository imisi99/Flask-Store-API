FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirement.txt . 
RUN pip install -r requirement.txt
COPY . .
CMD [ "flask", "run", "--host", "0.0.0.0" ]