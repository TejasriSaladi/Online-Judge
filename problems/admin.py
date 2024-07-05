from django.contrib import admin
from problems.models import Problem,TestCase,Solution

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id', 'level')
    search_fields = ('name', 'unique_id')
    list_filter = ('level','topic')

admin.site.register(Problem, ProblemAdmin)

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('input', 'output', 'problem_unique_id')
    list_filter = ('problem__unique_id',) 

    def problem_unique_id(self, obj):
        return obj.problem.unique_id

    problem_unique_id.admin_order_field = 'problem__unique_id'  # Allows ordering by this column in admin

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'verdict', 'submitted_at')
    list_filter = ('problem__unique_id',)

    def problem_unique_id(self, obj):
        return obj.problem.unique_id

    problem_unique_id.admin_order_field = 'problem__unique_id'  # Allows ordering by this column in admin
