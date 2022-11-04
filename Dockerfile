FROM python:3.11.0
# EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

# CMD [ "flask","run", "--host", "0.0.0.0" ]
# CMD [ "gunicorn","--bind", "0.0.0.0:80", "app:create_app()" ]
CMD ["/bin/bash", "docker-entrypoint.sh"]


