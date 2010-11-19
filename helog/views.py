from helog import app
from flask import render_template, request, flash, g, Response, url_for, Markup, redirect
from forms import HeTransferForm, create_choices
import model
import datetime
import csv
from xlwt import *
from xlwt.ExcelFormulaParser import FormulaParseException
from StringIO import StringIO

# n.b. Time allowed in javascript before udo link dissappears - request
# will be accepted for 15 extra second to allow for http lag
TIME_TO_UNDO = 30

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
        transfer['ip'] = request.remote_addr
        transfer['misc'] = '' # Somewhere to pickle some extra info in the future
        model.add_transfer(transfer)
        # Find out id of new transfer
        transfer = model.query_db('select * from entries order by time desc limit 1', one=True)
        id = transfer['id']
        flash(
            Markup('Success! - Transfer logged at %s <span id="undo_text">- <span id="undo_counter">%d</span> seconds to <a href="%s">Undo</a></span>' % (transfer['time'].strftime('%I:%M %p'), TIME_TO_UNDO, url_for('undo', id=id))), \
        'undo')
        # Reset the form
        form = HeTransferForm()
    elif request.method == 'POST' and not form.validate():
        flash('There was a problem with the submission ...', 'error')
    # Gather data for log
    transfers = model.query_db('select * from entries order by time desc limit 10')
##     transfers = transfers[:10]
    for t in transfers:
        # Put date in a nicer format
        t['time'] = t['time'].strftime('%d-%m-%y %I:%M %p')
    return render_template('index.html', form=form, transfers=transfers)

@app.route('/undo/<int:id>')
def undo(id):
    # Check ip matches and within timeframe
    transfer = model.query_db('select * from entries where id = ? limit 1', [id], one=True)
    secs_time_diff = (datetime.datetime.now() - transfer['time']).seconds
    # Note: allow slightly longer margin for undo than specified to take
    # into account http lag
    if (request.remote_addr == transfer['ip']) and (secs_time_diff < (TIME_TO_UNDO + 15)):
        model.delete_by_id(id)
        flash('Transfer aborted!', 'error')
    return redirect(url_for('index'))    

@app.route('/report')
def report_index():
    '''Generates links to all the reports'''
    return render_template('report_index.html', \
        users=create_choices(model.users), \
        meters=create_choices(model.meters), \
        transport_dewars=create_choices(model.transport_dewars), \
        cryostats = create_choices(model.cryostats) \
    )

@app.route('/report/html/<restrict_by>/<int:id>')
def report_html(restrict_by, id):
    '''Returns a report in html'''
    transfers = model.get_transfers(restrict_by, id)
    if restrict_by == 'user':
        val = model.users[id]
    elif restrict_by == 'meter':
        val = model.meters[id]
    elif restrict_by == 'transport_dewar':
        val = model.transport_dewars[id]
    elif restrict_by == 'cryostat':
        val = model.cryostats[id]
    return render_template('report.html', transfers=transfers, restrict_by=restrict_by, val=val)
    

@app.route('/report/csv/<restrict_by>/<int:id>')
def report_csv(restrict_by, id):
    '''Returns a report in csv format as a download'''
    transfers = model.get_transfers(restrict_by, id)
    out_stream = StringIO()
    out_stream.write('Name\tMeter\tMeter Before\tMeter After\tTransport Dewar\tTransport Dewar Before\tTransport Dewar After\tCryostat\tTime\n')
    csv_writer = csv.writer(out_stream, delimiter='\t')
    for t in transfers:
        csv_writer.writerow([t['user'], t['meter'], t['meter_before'], t['meter_after'], t['transport_dewar'], t['transport_dewar_before'], t['transport_dewar_after'], t['cryostat'], t['time']])
    return Response(out_stream.getvalue(), headers = {
        'Content-disposition' : 'application; filename=HeTransfers_%s%s.dat' % (restrict_by, id),
        'Content-Type' : 'text/css' }
    )
    

@app.route('/report/excel/<restrict_by>/<int:id>')
def report_excel(restrict_by, id):
    '''Returns a report in Excel format as a download'''
    transfers = model.get_transfers(restrict_by, id)
    # Work on the excel sheet
    header_style = XFStyle()
    header_style.font = Font()
    header_style.font.bold = True
    ws_title = 'He Transfer Data'
    ws_headers = (
        ('Time',),
        ('Meter', 'Name', 'Before', 'After'),
        ('Transport Dewar', 'Name', 'Before', 'After'),
        ('Cryostat',),
        ('Boiled Off During Transfer',),
        ('Litres Transferred',),
        ('Transferred By',),
    )
    w = Workbook()
    ws = w.add_sheet(ws_title)
    row_num = 0
    col_num = 0
    for header in ws_headers:
        if len(header) > 1:
            num_subheaders = len(header[1:])
            ws.write_merge(row_num, row_num, col_num, col_num+num_subheaders-1, header[0], header_style)
            for subheader in header[1:]:
                ws.write(row_num+1, col_num, subheader, header_style)
                col_num = col_num + 1
        else:    
            ws.write_merge(row_num, row_num+1, col_num, col_num, header[0], header_style)
            col_num = col_num + 1
            
    row_num = row_num + 1
    for i,t in enumerate(transfers):
        row_num = row_num + 1
        boiled_off = (t['meter_after'] - t['meter_before']) * 0.757
        amount_taken = t['transport_dewar_before'] - t['transport_dewar_after']
        ws.write(row_num, 0, t['time'].strftime('%d-%m-%Y %H:%M %p'))
        ws.write(row_num, 1, t['meter'])
        ws.write(row_num, 2, t['meter_before'])
        ws.write(row_num, 3, t['meter_after'])
        ws.write(row_num, 4, t['transport_dewar'])
        ws.write(row_num, 5, t['transport_dewar_before'])
        ws.write(row_num, 6, t['transport_dewar_after'])
        ws.write(row_num, 7, t['cryostat'])
        ws.write(row_num, 8, boiled_off)
        ws.write(row_num, 9, amount_taken)
        ws.write(row_num, 10, t['user'])
    out_stream = StringIO()
    w.save(out_stream)
    return Response(out_stream.getvalue(), headers = {
        'Content-disposition' : 'application; filename=HeTransfers_%s%s.xls' % (restrict_by, id),
        'Content-Type' : 'application/ms-excel' }
    )

# Run before every response request
@app.before_request
def before_request():
    g.db = model.connect_db()

# Run after every response request
@app.after_request
def after_request(response):
    g.db.close()
    return response

