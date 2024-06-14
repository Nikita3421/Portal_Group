from django.forms.models import inlineformset_factory

from . import models

ModuleFormSet = inlineformset_factory(
    models.Voting,
    models.VoteOption,
    fields=['title', 'description'],
    extra=2,
    can_delete=True,
)
