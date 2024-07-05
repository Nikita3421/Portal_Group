from django import forms
from grades.models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["user", "predmet", "ocenka", "comment"]
        

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})