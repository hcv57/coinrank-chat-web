import requests
from flask import Flask, render_template, url_for

app = Flask(__name__)

def calulate_change(current, previous):
    return "%.0f%%" % round((current - previous) / previous * 100, 2) if previous > 0 else ""

@app.route('/')
def home():
    r = requests.get('http://coinrank.chat/channels')
    fixme = []
    fixme.extend(r.json())
    fixme.extend(r.json())
    fixme.extend(r.json())
    fixme.extend(r.json())
    stats = [
        dict(rec,
             img_url=url_for('static', filename='1234.jpeg'),
             change_1h=calulate_change(rec['messages_1h'], rec['messages_prev_1h']),
             change_24h=calulate_change(rec['messages_24h'], rec['messages_prev_24h'])
             )
        for rec in fixme
    ]
    return render_template('home.html', entries=stats)
