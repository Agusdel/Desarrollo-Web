from flask import Flask
from flask import flash, render_template, request, url_for
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

class LinkForm(FlaskForm):
    text = StringField('Text')
    id = IntegerField('id', default=0)

class PassageForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()], default=0)
    paragraph = TextAreaField('Paragraph', validators=[DataRequired()], default="Type the paragraph...")
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
            'links': [{'text': form.links[0].data['text'], 'id': form.links[0].data['id']}]
        }
        passages.append(new_node)
        flash("Passage added")
    return render_template('edit.html', form=form, passages=passages)

@app.route('/passage/<int:passage_id>')
def show_passage(passage_id):
    if len(rewind_list) == 0 or rewind_list[-1] != passage_id:
        rewind_list.append(passage_id)
    return render_template("passage.html", passages=passages, passage_id=passage_id)

@app.route('/rewind')
def rewind():
    if len(rewind_list) == 0:
        previous_id = 1
    else:
        previous_id = rewind_list.pop()
    return render_template("passage.html", passages=passages, passage_id=previous_id)
        
if __name__ == "__main__":
    app.run()
