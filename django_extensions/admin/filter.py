from django.contrib.admin import FieldListFilter
from django.contrib.admin.utils import prepare_lookup_value
from django.utils.translation import gettext_lazy as _


class NullFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = "{0}__isnull".format(field_path)
        super().__init__(field, request, params, model, model_admin, field_path)
        lookup_choices = self.lookups(request, model_admin)
        self.lookup_choices = () if lookup_choices is None else list(lookup_choices)

    def expected_parameters(self):
        pass

    def value(self):
        pass

    def lookups(self, request, model_admin):
        pass

    def choices(self, cl):
        pass

    def queryset(self, request, queryset):
        pass


class NotNullFieldListFilter(NullFieldListFilter):
    def lookups(self, request, model_admin):
        pass
