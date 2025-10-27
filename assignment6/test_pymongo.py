from pymongo import MongoClient


client = MongoClient("mongodb://Ahmed:ahmed123@localhost:27017/")


db = client["AhmedDB"]
users = db["users"]


print("Liste users :")
for user in users.find():
    print(user)


new_user = {
    "name": "Ahmed",
    "email": "ahmed2@example.com",
    "profile": {"age": 30, "city": "Sfax"}
}
inserted_id = users.insert_one(new_user).inserted_id
print("\nNew user added with _id:", inserted_id)


users.update_one({"name": "Ahmed"}, {"$set": {"profile.city": "Monastir"}})
print("\n After update:")
for user in users.find({"name": "Ahmed"}):
    print(user)
