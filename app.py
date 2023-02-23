from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trimit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Urls(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(200), nullable=False)
    original_url = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.short_url}"
    
@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        short_url = request.form['short_url']
        original_url = request.form['original_url']
        url = Urls(short_url = short_url, original_url = original_url)
        db.session.add(url)
        db.session.commit()

    allUrls = Urls.query.all()
    return render_template('index.html', allUrls=allUrls)

@app.route('/about')
def products():
    allUrls = Urls.query.all()
    return render_template('about.html', allUrls=allUrls)

if __name__ =="__main__":
    app.run(debug=True)