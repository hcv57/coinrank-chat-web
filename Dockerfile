FROM python:alpine

WORKDIR /usr/src/app
RUN apk add --no-cache git
RUN pip install --no-cache-dir gunicorn git+https://github.com/coinrank/coinrank-chat-web#egg=coinrankchat_web
EXPOSE 8000
CMD ["gunicorn", "-w 3", "-b 0.0.0.0", "coinrankchat.web:app"]