from flask import Flask
from flask import flash, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, FormField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah-blah-secret-key'
Bootstrap(app)

rewind_list = []

### Example
node1 = {
    'id': '1',
    'paragraph': "Érase una vez una aventura de texto.",
    'links': [{ 'text': "Sigue por aquí", 'id': '2'}, {'text': "O mejor sigue por allá", 'id': '3'}]
}
###

passages = []

def find_passage_with_id(passage_id):
    for passage in passages:
        if passage['id'] == passage_id:
            return passage

    return None

class LinkForm(FlaskForm):
    text = StringField('Text')
    id = IntegerField('id', default=0)

class PassageForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()], default=0)
    paragraph = TextAreaField('Paragraph', validators=[DataRequired()], default="Type the paragraph...")
    background = StringField('Background Image', validators=[DataRequired()], default="background")
    links = FieldList(FormField(LinkForm), min_entries=3)
    submit = SubmitField('Add')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = PassageForm()
    if form.validate_on_submit():
        new_node = {
            'id': form.id.data,
            'paragraph': form.paragraph.data,
            'background': form.background.data,
            'links': []
        }
        for link in form.links:
            new_node['links'].append({'text': link.data['text'], 'id': link.data['id']})

        passages.append(new_node)
        flash("Passage added")
    return render_template('edit.html', form=form, passages=passages)

@app.route('/passage/<int:passage_id>')
def show_passage(passage_id):
    print ("")
    print ("/passage/%r" % passage_id)
    print ("")

    passage = find_passage_with_id(passage_id=passage_id)

    if passage is None:
        flash('Could not find passage with id %r' % passage_id)
        return redirect(url_for('index'))

    print (passage)

    is_first_passage = len(rewind_list) == 0

    rewind_list.append(passage_id)        

    return render_template("passage.html", passage=passage, is_first_passage=is_first_passage)

@app.route('/play')
def play():
    print ("")
    print ("/play")
    print ("")

    if len(passages) == 0:
        flash("You don't have any passages yet!")
        return redirect(url_for('index'))

    rewind_list = []
    return redirect(url_for('show_passage', passage_id=1))

@app.route('/rewind')
def rewind():
    print ("")
    print ("/rewind")
    print ("")

    # discards last element (its actually the current page)
    if len(rewind_list) > 0:
        rewind_list.pop()

    if len(rewind_list) == 0:
        print ("No previous page. Returning to home.")
        return redirect(url_for('index'))

    previous_id = rewind_list.pop()

    print ("rewinding to paragraph %r" % previous_id)
    print ("%r items left in rewind list" % len(rewind_list))


    return redirect(url_for('show_passage', passage_id=previous_id))
        
if __name__ == "__main__":
    app.run()
