import atexit
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy


class Config:
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///websites.db'


app = Flask(__name__)
app.config.from_object(Config())

# initialize db
db = SQLAlchemy(app)


# creta db
class Websites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    interval = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
def job1():
    test("https://google.com")


def blah():
    with scheduler.app.app_context():
        pass


def test(url):
    contents = requests.get(url)
    print(contents.status_code)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    title = "Home"
    if request.method == 'POST':
        website_title = request.form.get('title')
        website_url = request.form.get('url')
        monitor_interval = request.form.get('interval')

        new_wwebsite = Websites(title=website_title,
                                url=website_url,
                                interval=monitor_interval)

        # push to db
        try:
            db.session.add(new_wwebsite)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding website"
    else:
        websites = Websites.query.order_by(Websites.date_created)
        return render_template('index.html', title=title, websites=websites)


if __name__ == '__main__':
    app.run(debug=True)
