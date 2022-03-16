FROM python:3.10-slim-bullseye
WORKDIR /root/
COPY requirements.txt /root/
COPY app.py /root/
COPY ./app /root/app/
RUN pip install -r requirements.txt
CMD python /root/app.py

# docker build . -t foo
# docker run -e KENALL_API_TOKEN=$KENALL_API_TOKEN -e SLACK_APP_TOKEN=$SLACK_APP_TOKEN -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -it foo