from wtforms import Form, TextField, IntegerField, SelectField, ValidationError
from wtforms.validators import Required
from helog.model import users, cryostats, meters, transport_dewars

def create_choices(vals):
    'Choices argument requires key,val tuples tha are strings'
    return [(str(i), vals[i]) for i in range(len(vals))]

def validate_meter_field(form, field):
    test_str = field.data.replace('.', '')
    test_str = test_str.strip()
    for s in test_str:
        if s not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            raise ValidationError("Enter reading as #####.#")

def validate_dewar_field(form, field):
    test_str = field.data.strip()
    for s in test_str:
        if s not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            raise ValidationError("Enter an integer amount")

# Form for logging a He transfer
class HeTransferForm(Form):
    user = SelectField('Name', choices=create_choices(users))
    meter = SelectField('Meter', choices=create_choices(meters))
    meter_before = TextField('Before', \
        [Required(), validate_meter_field])
    meter_after = TextField('After', \
        [Required(), validate_meter_field])
    transport_dewar = SelectField('Transport Dewar', \
        choices=create_choices(transport_dewars))
    transport_dewar_before = TextField('Before', \
        [Required(), validate_dewar_field])
    transport_dewar_after = TextField('After', \
        [Required(), validate_dewar_field])
    cryostat = SelectField('Cryostat', \
        choices=create_choices(cryostats))
##     cryostat_before = IntegerField('Before', \
##         [Required(message='Enter a number with no decimal')])
##     cryostat_after = IntegerField('After', \
##         [Required(message='Enter a number with no decimal')])
