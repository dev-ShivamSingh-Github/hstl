from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_address(input_data):
    return True

def validate_name(input_data):
    if len(input_data) < 3:
        raise ValidationError(
                _('"%(input_data)s" is not a valid name'),
                params={"input_data": input_data},
                code='name',
        )
    if any(c.isdigit() for c in input_data):
        raise ValidationError(
                _('"%(input_data)s" is not a valid name. Contains digit'),
                params={"input_data": input_data},
                code='name',
        )
    if not input_data.strip().replace(' ', '').isalpha():
        raise ValidationError(
                _('"%(input_data)s" is not a valid name. Contains special characters'),
                params={"input_data": input_data},
                code='name',
        )
    return True

def validate_mobile(input_data):
    if (
        len(input_data) != 10 or
        input_data[0] in "012345" or
        not input_data.isdigit()
        ):
        raise ValidationError(
                _('"%(input_data)s" is not a valid mobile number'),
                params={"input_data": input_data},
                code='mobile',
        )
    return True

def validate_password(input_data):
    if len(input_data) < 10:
        raise ValidationError(
                _('Password should have at least 10 characters'),
                code='password',
        )
    if not any(c.isupper() for c in input_data):
        raise ValidationError(
                _('Password should have at least one upper case alphabet'),
                code='password',
        )
    if not any(c.islower() for c in input_data):
        raise ValidationError(
                _('Password should have at least one lower case alphabet'),
                code='password',
        )
    if not any(c.isdigit() for c in input_data):
        raise ValidationError(
                _('Password should contain digit'),
                code='password',
        )
    if not any(c in '!@#$%^&*()_=+-/.' for c in input_data):
        raise ValidationError(
                _('Password should have at least one special symbol: !@#$%^&*()_=+-/.'),
                code='password',
        )
    return True

def validate_aadhar(input_data):
    if not input_data.isdigit():
        raise ValidationError(
                _('Aadhar number should only contain digit'),
                code='aadhar',
        )
    if len(input_data) != 12:
        raise ValidationError(
                _('Aadhar number should have 12 digits only'),
                code='aadhar',
        )
    return True
