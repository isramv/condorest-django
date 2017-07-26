from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm
from django.utils.translation import ugettext_lazy as _

from revenue.models import Receipt, FeeLine


class FeeLinesInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(FeeLinesInlineFormSet, self).clean()

        total = 0
        for form in self.forms:
            if not form.is_valid() or form.cleaned_data.get('DELETE'):
                return # there are other errors in the form or the item was deleted
            total += form.cleaned_data.get('amount', 0)

        self.instance.total_amount = total
        print(self.instance)


class FeeLineForm(ModelForm):
    def clean(self):
        if self.cleaned_data['date_start'] > self.cleaned_data['date_end']:
            raise ValidationError(_("Date start must be before date end"))


class FeeLinesInline(admin.TabularInline):
    form = FeeLineForm
    model = FeeLine
    formset = FeeLinesInlineFormSet
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        # Don't add any extra forms if the related object already exists.
        if obj:
            return 0
        return self.extra


class ReceiptAdmin(admin.ModelAdmin):
    readonly_fields = ['total_amount']
    inlines = [FeeLinesInline]


admin.site.register(Receipt, ReceiptAdmin)
