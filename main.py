from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import json
from datetime import datetime
from flask_mail import Mail



with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# local_server = True


app = Flask(__name__)
app.config['MYSQL_HOST'] = params['host']
app.config['MYSQL_PORT'] = params['port']
app.config['MYSQL_USER'] = params['user']
app.config['MYSQL_PASSWORD'] = params['password']
app.config['MYSQL_DB'] = params['database']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_CONNECT_TIMEOUT'] = 60 # 5 minutes

# Initialize MySQL
db = MySQL(app)

# mail configuration
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
    

@app.route("/")
def home():

    return render_template('index.html', params=params)

@app.route("/about")
def about():

    return render_template('about.html', params=params)

@app.route("/service")
def service():

    return render_template('service.html', params=params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        date= datetime.now()


        # Insert the form data into MySQL
        cur = db.connection.cursor()
        cur.execute("INSERT INTO contacts (name, mobile, email, subject, msg, date) VALUES (%s, %s, %s, %s, %s, %s)", (name, number, email, subject, message, date))
        db.connection.commit()
        cur.close()


        #send response mail
        mail.send_message('New query from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = "Client Name :  " + name + "\n" + "Client Number :  " + number + "\n" + "Client Mail Id :  " + email + "\n" + "Query Subject :  " + subject + "\n\n\n\n" + "Message :  " + message
                          )


        return render_template('contact.html', params=params)
    
    else:
        return render_template('contact.html', params=params)


@app.route("/insight")
def insight():

    return render_template('insight.html', params=params)

@app.route("/insight1")
def insight1():

    return render_template('insight1.html', params=params)


@app.route("/insight2")
def insight2():

    return render_template('insight2.html', params=params)


@app.route("/insight3")
def insight3():

    return render_template('insight3.html', params=params)



@app.route('/news')
def news():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM news_post ORDER BY date DESC")
    data = cur.fetchall()
    return render_template('news.html', news=data, params=params)

@app.route('/post/<string:post_slug>/')
def post_route(post_slug):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM news_post WHERE slug=%s", (post_slug,))
    data = cur.fetchone()
    return render_template('post.html', post=data, params=params)



@app.route("/service1")
def service1():

    return render_template('service1.html', params=params)

@app.route("/service2")
def service2():

    return render_template('service2.html', params=params)

@app.route("/service3")
def service3():

    return render_template('service3.html', params=params)

@app.route("/service4")
def service4():

    return render_template('service4.html', params=params)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)