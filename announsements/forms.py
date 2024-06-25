from django import forms
from announsements.models import Announsement

class AnnounsementForm(forms.ModelForm):
    class Meta:
        model = Announsement
        fields = ["title", "text", "media"]
        widgets = {
            "media": forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super(AnnounsementForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        #self.fields["creation_date"].widget.attrs["class"] += " my-custom=datepicker"

