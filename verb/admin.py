import csv
import openpyxl
from django.contrib import admin, messages
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from verb.models import VerbCategory, Verb


class CsvForm(forms.Form):
    csv_upload = forms.FileField(label=False)

    def __init__(self, *args, **kwargs):
        super(CsvForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'


@admin.register(VerbCategory)
class VerbCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_per_page = 200
    list_display = (
        'infinitive', 'english_translation', 'danish_translation', 'category', 'eu', 'voce_ele_ela', 'nos',
        'voces_eles_elas')
    list_editable = (
    'english_translation', 'danish_translation', 'category', 'eu', 'voce_ele_ela', 'nos', 'voces_eles_elas')
    search_fields = ['infinitive', 'english_translation', 'danish_translation']
    ordering = ['-id']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('upload-csv/', self.upload_csv)]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES["csv_upload"]
            csv_cat = request.POST["category"]

            if csv_file.name.endswith('.csv'):
                file_data = csv_file.read().decode("utf-8")
                csv_data = csv.reader(file_data.splitlines(), delimiter=',')
                next(csv_data)  # Skip the header row

                for row in csv_data:
                    if len(row) == 7:
                        infinitive, english_translation, danish_translation, eu, voce_ele_ela, nos, voces_eles_elas = row
                        created = Verb.objects.update_or_create(
                            infinitive=infinitive,
                            english_translation=english_translation,
                            danish_translation=danish_translation,
                            eu=eu,
                            voce_ele_ela=voce_ele_ela,
                            nos=nos,
                            voces_eles_elas=voces_eles_elas,
                            lang_category_id=csv_cat,
                        )

            elif csv_file.name.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(csv_file)
                sheet = workbook.active

                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if len(row) == 7:
                        infinitive, english_translation, danish_translation, eu, voce_ele_ela, nos, voces_eles_elas = row
                        created = Verb.objects.update_or_create(
                            infinitive=infinitive,
                            english_translation=english_translation,
                            danish_translation=danish_translation,
                            eu=eu,
                            voce_ele_ela=voce_ele_ela,
                            nos=nos,
                            voces_eles_elas=voces_eles_elas,
                            category_id=csv_cat,
                        )

            else:
                messages.warning(request, "Only CSV and XLSX files are allowed")
                return HttpResponseRedirect(request.path_info)

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvForm()
        category = VerbCategory.objects.all()
        data = {
            "category": category,
            "form": form
        }
        return render(request, "admin/upload_csv.html", data)
