import requests
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///websites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create db


class Websites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255))
    interval = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


codes = []


def show_websites():
    """Print all websites status code."""
    asyncio.sleep(1)
    with db.app.app_context():
        for website in Websites.query.all():
            codes.append(test(website.url))

    return codes


def test(url):
    contents = requests.get(url)
    return contents.status_code


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    title = "Home"
    if request.method == 'POST':
        website_title = request.form.get('title')
        website_url = request.form.get('url')
        monitor_interval = request.form.get('interval')
        website_status = test(website_url)

        new_website = Websites(title=website_title,
                               url=website_url,
                               interval=monitor_interval,
                               status=website_status)
        # push to db
        try:
            db.session.add(new_website)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding website"
    else:
        websites = Websites.query.order_by(Websites.date_created)
        return render_template('index.html', title=title, websites=websites)


if __name__ == '__main__':
    # app.config.from_object(Config())

    # db.init_app(app)

    app.run(debug=True)
