from helog import app
from flask import render_template, request, flash, g
from forms import HeTransferForm, create_choices
import model
import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    # Gather data from form
    form = HeTransferForm(request.form)
    if request.method == 'POST' and form.validate():
        transfer = request.form.copy()
        transfer['user'] = model.users[int(transfer['user'])]
        transfer['meter'] = model.meters[int(transfer['meter'])]
        transfer['transport_dewar'] = model.transport_dewars[int(transfer['transport_dewar'])]
        transfer['cryostat'] = model.cryostats[int(transfer['cryostat'])]
        transfer['time'] = datetime.datetime.now()
        model.add_transfer(transfer)
        flash('Success!')
    # Gather data for log
    transfers = model.query_db('select * from entries order by time limit 10')
    for t in transfers:
        # Put date in a nicer format
        t['time'] = datetime.datetime.strptime(t['time'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d-%m-%y %I:%M %p')
    return render_template('index.html', form=form, transfers=transfers)

@app.route('/report'):
    '''Generates links to all the reports'''
    return render_template('report_index.html', \
        users=create_choices(model.users), \
        meters=create_choices(model.meters), \
        transport_dewars=create_choices(model.transport_dewars), \
        cryostats = create_choices(model.cryostats) \
    )

# Run before every response request
@app.before_request
def before_request():
    g.db = model.connect_db()

# Run after every resposne request
@app.after_request
def after_request(response):
    g.db.close()
    return response
