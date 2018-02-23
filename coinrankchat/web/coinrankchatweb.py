import requests
from flask import Flask, render_template, url_for
from . import config

app = Flask(__name__)

def calulate_change(current, previous):
    return "%.0f%%" % round((current - previous) / previous * 100, 2) if previous > 0 else ""

@app.route('/')
def home():
    r = requests.get('http://%s/api/channels' % config.API_SERVER_HOST)
    stats = [
        dict(rec,
             img_url=url_for('static', filename='%s/%s.jpeg' % (config.IMAGE_SERVER_URL, rec['channel_id'])),
             change_1h=calulate_change(rec['messages_1h'], rec['messages_prev_1h']),
             change_24h=calulate_change(rec['messages_24h'], rec['messages_prev_24h'])
             )
        for rec in r.json()
    ]
    return render_template('home.html', entries=stats)
