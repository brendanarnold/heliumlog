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
    meter_before = IntegerField('Meter Before', [Required()])
    meter_after = IntegerField('Meter After', [Required()])
    transport_dewar = SelectField('Transport Dewar', choices=create_choices(transport_dewars))
    transport_dewar_before = IntegerField('Transport Dewar Before', [Required()])
    transport_dewar_after = IntegerField('Transport Dewar After', [Required()])
    cryostat = SelectField('Cryostat', choices=create_choices(cryostats))
    cryostat_before = IntegerField('Cryostat Before', [Required()])
    cryostat_after = IntegerField('Cryostat After', [Required()])
