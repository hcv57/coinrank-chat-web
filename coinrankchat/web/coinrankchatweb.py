import requests
from flask import Flask, render_template, url_for
from slugify import slugify

from . import config

app = Flask(__name__)

def calulate_change(current, previous):
    return "%.0f%%" % round((current - previous) / previous * 100, 2) if previous > 0 else ""

@app.route('/')
def home():
    r = requests.get('http://%s/api/groups' % config.API_SERVER_HOST)
    entries = [
        dict(rec,
             group_url=url_for('group', channel_id=rec['channel_id'], slug=slugify(rec['title'])),
             img_url='%s/%s.jpeg' % (config.IMAGE_SERVER_URL, rec['channel_id']),
             change_1h=calulate_change(rec['messages_1h'], rec['messages_prev_1h']),
             change_24h=calulate_change(rec['messages_24h'], rec['messages_prev_24h'])
             )
        for rec in r.json()
    ]
    return render_template('home.html', entries=entries)

@app.route('/group/<channel_id>/<slug>')
def group(channel_id, slug):
    entry = dict(
        img_url_big = '%s/%s-big.jpeg' % (config.IMAGE_SERVER_URL, channel_id)
    )
    return render_template('group.html', entry=entry)