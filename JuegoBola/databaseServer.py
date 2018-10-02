import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    highscore = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():

    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        session['name'] = form.name.data
        if user is None:
            user = User(username=form.name.data, highscore=0)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            session['highscore'] = user.highscore
            return redirect(url_for('ballgame'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))

def print_submited_values(player, score):
    print("Player " + str(player) + " submitted score " + str(score) + ".")

@app.route('/submit', methods=['POST'])
def submit_score():
    player = request.form.get('player', type = str)
    score = request.form.get('score', default = 0, type = int)

    #print_submited_values(player, score);

    session['name'] = player

    user = User.query.filter_by(username=player).first()
    if (score > user.highscore):
        user.highscore = score
        db.session.commit()
        
    session['highscore'] = score

    return redirect(url_for('index'))


@app.route('/ballgame', methods=['GET', 'POST'])
def ballgame():
    return render_template('ballgame.html', player=session.get('name'), highscore=session.get('highscore'))
                           
if __name__ == '__main__':
	db.drop_all()
	db.create_all()
	app.run()
