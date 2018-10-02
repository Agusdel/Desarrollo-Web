import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


def dictToList(d):
    l = list(d.values())
    pageList = []

    for e in l:
        print (e)

    for e in l:
        if e is not None:
            page = StoryPage(name=e["name"], text=e["text"], link1Name=e["link1Name"], link1Text=e["link1Text"])
            if page is not None:
                pageList.append(page)

    return pageList

def listToDict(l):
    d = {}
    for page in l:
        d[page.__repr__] = page.toDict()
    return d


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


class StoryPage(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    text = db.Column(db.String(1024))
    link1Name = db.Column(db.String(64))
    link1Text = db.Column(db.String(128))

    def __repr__(self):
        return '<Page %r>' % self.name

    def toDict(self):
        d = {}
        d["name"] = self.name
        d["text"] = self.text
        d["link1Name"] = self.link1Name
        d["link1Text"] = self.link1Text


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ParagraphForm(FlaskForm):
    name = StringField('What is the page name?', [DataRequired(), Length(min=4, max=64)])
    text = StringField('What is the page content?', [DataRequired(), Length(min=4, max=1024)])
    link1Name = StringField('Would you like to link this page to another one? Which one?', [Length(max=64)])
    link1Text = StringField('Link text?', [Length(max=128)])
    submit = SubmitField('Add Page')


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
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/editor', methods=['GET', 'POST'])
def editor():

    form = ParagraphForm()
    pageList = []

    page1 = StoryPage(name='Page 1', text="This is my first page", link1Name='Page 2', link1Text="Go to page 2")
    page2 = StoryPage(name='Page 2', text="This is my second page")

    pageList.append(page1)
    pageList.append(page2)
    #pageDict = session.get('pageDict')
    #if pageDict is not None:
    #    pageList = dictToList(pageDict)

    #session['pageDict'] = listToDict(pageList)
    if form.validate_on_submit() and form.name.data is not None:
        newPage = StoryPage(name=form.name.data, text=form.text.data, link1Name=form.link1Name.data, link1Text=form.link1Text.data)
        print (newPage)
        pageList.append(newPage)

        session['pageDict'] = listToDict(pageList)

        print ("page added to list")

    return render_template('editor.html', form=form, pageList=pageList)
                           
if __name__ == '__main__':
	db.drop_all()
	db.create_all()
	app.run()