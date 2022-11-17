from django.contrib import admin

from .models import (
    Interest, LoanLevel, UserLoan, LoanRepayment, LoanPurpose, Guarntee, InterestBreakdown, HomePagePromotion, RepaymentGuide,LoanPageInformationSlider
)


admin.site.register(Interest)
admin.site.register(LoanLevel)
admin.site.register(UserLoan)
admin.site.register(LoanRepayment)
admin.site.register(LoanPurpose)
admin.site.register(Guarntee)
admin.site.register(InterestBreakdown)
admin.site.register(HomePagePromotion)
admin.site.register(RepaymentGuide)
admin.site.register(LoanPageInformationSlider)








