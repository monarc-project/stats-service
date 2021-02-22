#! /bin/sh

pybabel extract -F statsservice/translations/babel.cfg -k lazy_gettext -o statsservice/translations/messages.pot statsservice/

#poedit statsservice/translations/fr_FR/LC_MESSAGES/messages.po
