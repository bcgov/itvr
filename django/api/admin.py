from django.contrib import admin

from .models.income_verification import IncomeVerification, IncomeVerificationImage

admin.site.register(IncomeVerification)
admin.site.register(IncomeVerificationImage)
