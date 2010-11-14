from helog import app
from flask import render_template, request, flash, g, Response
from forms import HeTransferForm, create_choices
import model
import datetime
import csv
from xlwt import *
from xlwt.ExcelFormulaParser import FormulaParseException
from StringIO import StringIO


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
        flash('Success! - Transfer logged at %s' % transfer['time'].strftime('%I:%M %p'), 'ok')
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
    out_stream.write('Name\tMeter\tMeter Before\tMeter After\tTransport Dewar\tTransport Dewar Before\tTransport Dewar After\tCryostat\tCryostat Before\tCryostat After\tTime\n')
    csv_writer = csv.writer(out_stream, delimiter='\t')
    for t in transfers:
        csv_writer.writerow([t['user'], t['meter'], t['meter_before'], t['meter_after'], t['transport_dewar'], t['transport_dewar_before'], t['transport_dewar_after'], t['cryostat'], t['cryostat_before'], t['cryostat_after'], t['time']])
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
        ('Dewar', 'Name', 'Before', 'After'),
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
        ws.write(row_num, 8, t['cryostat_before'])
        ws.write(row_num, 9, t['cryostat_after'])
        ws.write(row_num, 10, boiled_off)
        ws.write(row_num, 11, amount_taken)
        ws.write(row_num, 12, t['user'])
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

