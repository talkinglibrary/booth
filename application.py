'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from datetime import datetime
from flask import Flask, render_template, request

from hours import hour1, hour2
from scrape import scrape, check_banner
from icecast import icecast_now_playing

application = Flask(__name__)

def are_we_closed():
    current_hour = datetime.now().strftime('%H')
    current_hour = int(current_hour)

    current_day = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']

    if current_hour < 8 or current_hour > 16:
        return True

    if current_day in weekend:
        return True
    
    return False

@application.route('/live')
def homepage():
    if are_we_closed():
        return render_template('closed.html')

    booth1, booth2, booth3, booth1_2, booth2_2, booth3_2 = scrape()
    
    return render_template('home.html', booth1=booth1, booth2=booth2, booth3=booth3,\
        booth1_2=booth1_2, booth2_2=booth2_2, booth3_2=booth3_2, hour=hour1(), hour2=hour2(), banner=check_banner())

@application.route('/health')
def health_check():
    '''for AWS EB's health check'''
    return "<div style='font-size: 85pt; text-align: center;'>I AM WORKING FINE</div>" 

@application.route('/')
def dot():
    if are_we_closed():
        return render_template('closed.html')

    return render_template('land.html')

'''
just using this route for testing styles and such so we don't
need to run selenium every time we want to reload the page.
'''
@application.route('/test')
def testing():
    return render_template('home.html', booth1='Test Nobody', booth2='Test Nobody', booth3='Test Nobody',\
        booth1_2='Test Nobody', booth2_2='Test Nobody', booth3_2='Test Nobody', hour=hour1(), hour2=hour2(), banner=check_banner())

@application.route('/banner', methods=['GET', 'POST'])
def banner():
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        if user == 'talk5874':
            with open('message.txt', 'w') as text:
                text.write(message)
                text.close()
            return render_template('banner.html', emoji='&#128077;') # thumbs up
        else:
            return render_template('banner.html', emoji='&#128078;') # thumbs down
    return render_template('banner.html')

@application.route('/nowplaying')
def now_playing():
    return icecast_now_playing()

# do something to explicitly handle HTTP errors so we don't get some general nginx page

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

@application.errorhandler(500)
def handle_exception(e):
    return render_template("broken.html", e=e), 500
    

if __name__ == '__main__':
    application.run()