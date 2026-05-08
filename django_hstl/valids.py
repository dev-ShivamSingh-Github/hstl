# my validations...
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_address(input_data):
    return True

def validate_name(input_data):
    if any(c.isdigit() for c in input_data):
        raise ValidationError(
                _('%(input_data) is not a valid name. Contains digit'),
                params={"input_data": input_data},
                code='name',
        )
    return True

def validate_mobile(input_data):
    if not (
        len(input_data) == 10 and
        input_data[0] not in "012345" and
        all(c.isdigit() for c in input_data)
        ):
        raise ValidationError(
                _('%(input_data) is not a valid mobile number'),
                params={"input_data": input_data},
                code='mobile',
        )
    return True

def validate_password(input_data):
    if len(input_data) < 8:
        raise ValidationError(
                _('Password should have at least 8 characters'),
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
    if not all(c.isdigit() for c in input_data):
        raise ValidationError(
                _('Aadhar number should only contain digit'),
                code='aadhar',
        )
    if len(input_data) < 12:
        raise ValidationError(
                _('Invalid aadhar number'),
                code='aadhar',
        )
    return True
