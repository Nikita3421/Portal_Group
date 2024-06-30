from django.forms.models import inlineformset_factory

from . import models

OptionFormSet = inlineformset_factory(
    models.OptionQuestion,
    models.Option,
    fields=['title', ],
    extra=2,
    can_delete=True,
)
