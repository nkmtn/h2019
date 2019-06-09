# Turn off bytecode generation
import json
import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()

from django.core import serializers
from db.models import *

# Start of application script
for u in User.objects.all():
	print("ID: " + str(u.id) + "\tUsername: " + u.first_name)


class UserData:
	def getUserInfo(self, id):
		u = User.objects.get(id=id)

		result = serializers.serialize("json", [u])

		return result

	def setUserInfo(self, id, data):
		u = User.objects.get(id=id)
		json_dict = json.loads(data)
		u.first_name = data['first_name']
		u.save()

class AchievementData:
	pass


u = UserData()
u.getUserInfo(14)



