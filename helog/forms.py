from wtforms import Form, TextField, IntegerField, SelectField
from wtforms.validators import Required
from helog.model import users, cryostats, meters, transport_dewars

def create_choices(vals):
    'Choices argument requires key,val tuples tha are strings'
    return [(str(i), vals[i]) for i in range(len(vals))]

# Form for logging a He transfer
class HeTransferForm(Form):
    user = SelectField('Name', choices=create_choices(users))
    meter = SelectField('Meter', choices=create_choices(meters))
    meter_before = IntegerField('Before', \
        [Required(message='Enter a number with no decimal')])
    meter_after = IntegerField('After', \
        [Required(message='Enter a number with no decimal')])
    transport_dewar = SelectField('Transport Dewar', choices=create_choices(transport_dewars))
    transport_dewar_before = IntegerField('Before', \
        [Required(message='Enter a number with no decimal')])
    transport_dewar_after = IntegerField('After', \
        [Required(message='Enter a number with no decimal')])
    cryostat = SelectField('Cryostat', choices=create_choices(cryostats))
##     cryostat_before = IntegerField('Before', \
##         [Required(message='Enter a number with no decimal')])
##     cryostat_after = IntegerField('After', \
##         [Required(message='Enter a number with no decimal')])
