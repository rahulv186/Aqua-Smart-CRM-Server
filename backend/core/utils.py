import string
from django.utils.crypto import get_random_string

def generate_unique_code(model_class, field_name, prefix="EMP", length=6):
    # Example: EMP-7K3X9M, CUST-2W8Y1P
    
    while True:
        # Generate uppercase alphanumeric random string
        random_str = get_random_string(
            length=length, 
            allowed_chars=string.ascii_uppercase + string.digits
        )
        code = f"{prefix}-{random_str}"
        
        # Check database to ensure absolute uniqueness (prevents IntegrityError)
        if not model_class.objects.filter(**{field_name: code}).exists():
            return code