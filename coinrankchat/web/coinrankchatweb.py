import requests
from flask import Flask, render_template, url_for
from markdown import markdown
from slugify import slugify

from . import config

app = Flask(__name__)

def calulate_change(current, previous):
    return "%.1f%%" % round((current - previous) / previous * 100, 2) if previous > 0 else ""

@app.route('/')
def home():
    api_response = requests.get('http://%s/api/groups' % config.API_SERVER_HOST).json()
    response = list(filter(
        lambda g: g['before_yesterday']['num_messages'] > 0 and
                  g['yesterday']['num_messages'] > 0 and
                  g['today']['num_messages'] > 0
        , api_response))

    yesterdays_group_ranking = dict([
        (group['_id'], i)
        for (i, group) in enumerate(sorted(response, key=lambda g: g['yesterday']['distinct_participants'], reverse=True))
    ])

    groups = [
        dict(
            rank=i+1,
            yesterdays_rank=yesterdays_group_ranking[rec['_id']] + 1,
            rank_change="%+d" % (yesterdays_group_ranking[rec['_id']] - i),
            title=rec['title'],
            group_url=url_for('group', _id=rec['_id'], slug=slugify(rec['title'])),
            img_url='%s/%s.jpeg' % (config.IMAGE_SERVER_URL, rec['channel_id']),
            num_messages=rec['today']['num_messages'],
            num_participants=rec['today']['max_participants'],
            global_sentiment_average=rec['global_sentiment_average'],
            sentiment_today=rec['today']['sentiment_average'] or 0,
            sentiment_yesterday=rec['yesterday']['sentiment_average'] or 0,
            delta_messages="%+d" % (rec['today']['num_messages'] - rec['yesterday']['num_messages']),
            delta_messages_percentage=calulate_change(rec['today']['num_messages'], rec['yesterday']['num_messages']),
            delta_participants="%+d" % (rec['today']['max_participants'] - rec['yesterday']['max_participants']),
            delta_participants_percentage=calulate_change(rec['today']['max_participants'], rec['yesterday']['max_participants'])
            )
        for (i, rec) in enumerate(sorted(response, key=lambda c: c['today']['distinct_participants'], reverse=True))
    ]

    return render_template('home.html', groups=groups)

@app.route('/g/<_id>/<slug>')
def group(_id, slug):
    r = requests.get('http://%s/api/group/%s' % (config.API_SERVER_HOST, _id))
    entry = r.json()
    entry.update(
        img_url_big = '%s/%s-big.jpeg' % (config.IMAGE_SERVER_URL, entry['channel_id']),
        about = markdown(entry.get('about', 'No description available at this time.'), extensions=["mdx_linkify"]),
        pinnedMessage = markdown(entry.get('pinnedMessage', 'There is no pinned message.'), extensions=["mdx_linkify"])
    )
    return render_template('group.html', entry=entry)