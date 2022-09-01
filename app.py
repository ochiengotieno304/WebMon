import atexit
import requests
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

websites = []


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    title = "Home"
    if request.method == 'POST':
        website_title = request.form.get('title')
        website_url = request.form.get('url')
        monitor_interval = request.form.get('interval')

        status_code = test(website_url)

        websites.append(f"{website_title} {website_url} {monitor_interval} {status_code}")
    

    return render_template('index.html', title=title, websites=websites)


def test(url):
    contents = requests.get(url)
    return contents.status_code


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=test, trigger="interval", seconds=10)
# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(debug=True)
