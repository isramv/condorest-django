from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _

from revenue.models import Receipt, FeeLine, Fee


class FeeLinesInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(FeeLinesInlineFormSet, self).clean()

        total = 0
        for form in self.forms:
            if not form.is_valid() or form.cleaned_data.get('DELETE'):
                continue # there are other errors in the form or the item was deleted
            total += form.cleaned_data.get('amount', 0)

        if (total != self.instance.amount):
            raise ValidationError(_("FeeLine amounts must add up to the receipt amount."))


class FeeLineForm(forms.ModelForm):
    def clean(self):
        pass


class FeeLinesInline(admin.TabularInline):
    form = FeeLineForm
    model = FeeLine
    formset = FeeLinesInlineFormSet
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        """Don't add any extra forms if the related object already exists."""
        if obj:
            return 0
        return self.extra


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['date', 'number', 'save_in_ledger', 'details_summary', 'contact', 'debit_account', 'credit_account', 'amount']
    list_filter = ['date', 'save_in_ledger']
    list_select_related = ['contact', 'debit_account', 'credit_account']
    fields = ('date', 'contact', 'number', 'details', 'debit_account', 'credit_account', 'amount', 'save_in_ledger')
    inlines = [FeeLinesInline]
    search_fields = ['number', 'details']
    ordering = ['-date']


class FeeAdmin(admin.ModelAdmin):
    list_display = ['date', 'lot', 'amount']
    list_filter = ['date']
    list_select_related = ['lot']
    search_fields = ['lot__name']


admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Fee, FeeAdmin)
