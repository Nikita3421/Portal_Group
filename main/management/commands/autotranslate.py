from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from translate import Translator
from pathlib import Path
import polib
import os
import requests

class Command(BaseCommand):
    help = 'automatically translate messages using translate lib'
    
    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)
    
    def translate_text(self,text, target_language):
        translator= Translator(to_lang=target_language)
        return translator.translate(text)
    
    def handle(self, *args, **options):
        
        
        for lang in settings.LANGUAGES:
            lang_code = lang[0]
            path = os.path.join(settings.LOCALE_PATHS[0],lang_code,'LC_MESSAGES/django.po')
            po = polib.pofile(path)
            for entry in po.untranslated_entries():
                try:
                    translated_text = self.translate_text(entry.msgid, lang_code)
                except requests.exceptions.ReadTimeout:
                    pass
                entry.msgstr = translated_text
            po.save()


