FROM python:3.10
WORKDIR /app
COPY requirement.txt . 
RUN pip install --no-cache-dir --install -r requirement.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]