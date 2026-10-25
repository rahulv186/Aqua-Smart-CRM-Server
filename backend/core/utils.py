import string
from django.utils.crypto import get_random_string
from rest_framework.permissions import BasePermission


def generate_unique_code(model_class, field_name, prefix="EMP", length=6):
    # Example: EMP-7K3X9M, CUST-2W8Y1P

    while True:
        # Generate uppercase alphanumeric random string
        random_str = get_random_string(
            length=length, allowed_chars=string.ascii_uppercase + string.digits
        )
        code = f"{prefix}-{random_str}"

        # Check database to ensure absolute uniqueness (prevents IntegrityError)
        if not model_class.objects.filter(**{field_name: code}).exists():
            return code


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        # Checks if user is logged in AND is a superuser
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsOwnerOfCompany(BasePermission):
    """
    Ensures the user is an owner AND belongs to the specific company in the URL slug.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if not hasattr(request.user, "company_owner_profile"):
            return False

        # Grab the company_slug from the URL kwargs passed to the view
        company_slug = view.kwargs.get("company_slug")
        if not company_slug:
            return True  # Fallback if slug isn't in URL

        # Verify tenant match
        return request.user.company_owner_profile.company.slug == company_slug


class IsManager(BasePermission):
    """
    Allows access only to users who are managers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(
                request.user, "manager_profile"
            )  # Adjust if your manager model uses a different related_name or field
        )


class IsOwnerOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.user)
            and (request.user.is_authenticated)
            and (
                (hasattr(request.user, "manager_profile"))
                or hasattr(request.user, "company_owner_profile")
            )
        )
