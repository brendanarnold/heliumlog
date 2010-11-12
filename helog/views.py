from helog import app
from flask import render_template, request, flash
from forms import HeTransferForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HeTransferForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Success!')
    return render_template('index.html', form=form)
