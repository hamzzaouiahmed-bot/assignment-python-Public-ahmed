from mongoengine import *

connect(db="AhmedDB", host="localhost", port=27017, username="Ahmed", password="ahmed123")

class Profile(EmbeddedDocument):
    age = IntField()
    city = StringField()

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)

print("users existants :")
for u in User.objects():
    print(u.to_json())


u = User(name="Alex", email="alex2@example.com", profile=Profile(age=35, city="Sfax"))
u.save()
print("\n new user add:")
print(u.to_json())


user = User.objects(name="Alex").first()
user.profile.city = "Monastir"
user.save()
print("\nAfter update:")
print(user.to_json())
