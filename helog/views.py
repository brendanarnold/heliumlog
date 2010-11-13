from helog import app
from flask import render_template, request, flash, g
from forms import HeTransferForm
import model
import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    # Gather data from form
    form = HeTransferForm(request.form)
    if request.method == 'POST' and form.validate():
        user = model.users[int(request.form['user'])]
        meter = model.meters[int(request.form['meter'])]
        transport_dewar = model.transport_dewars[int(request.form['transport_dewar'])]
        cryostat = model.cryostats[int(request.form['cryostat'])]
        g.db.execute('insert into entries (user, meter, meter_before, ' \
            + 'meter_after, transport_dewar, transport_dewar_before, ' \
            + 'transport_dewar_after, cryostat, cryostat_before, ' \
            + 'cryostat_after, time) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ' \
            + '?, ?)', [user, meter, request.form['meter_before'], \
            request.form['meter_after'], transport_dewar, \
            request.form['transport_dewar_before'], \
            request.form['transport_dewar_after'], \
            cryostat, request.form['cryostat_before'], \
            request.form['cryostat_after'], datetime.datetime.now()])
        g.db.commit()
        flash('Success!')
    # Gather data for log
    cursor = g.db.execute('select * from entries order by time')
    transfers = []
    for t in cursor.fetchall():
        d = dict()
        d['user'] = t[1]
        d['meter'] = t[2]
        d['meter_before'] = t[3]
        d['meter_after'] = t[4]
        d['transport_dewar'] = t[5]
        d['transport_dewar_before'] = t[6]
        d['transport_dewar_after'] = t[7]
        d['cryostat'] = t[8]
        d['cryostat_before'] = t[9]
        d['cryostat_after'] = t[10]
        d['time'] = datetime.datetime.strptime(t[11], '%Y-%m-%d %H:%M:%S.%f').strftime('%d-%m-%y %I:%M %p')
        transfers.append(d)
    return render_template('index.html', form=form, transfers=transfers)

# Run before every response request
@app.before_request
def before_request():
    g.db = model.connect_db()

# Run after every resposne request
@app.after_request
def after_request(response):
    g.db.close()
    return response
