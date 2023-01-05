# import hashlib

# passwd = "frankdony"
# hashed_passwd = "360b8b4e655b73533768dae611816eb6"
# hashed = hashlib.md5(passwd.encode('utf-8')).hexdigest()
# print(hashed == hashed_passwd)

from models import storage
users = [user.id[:8] for user in storage.all("User").values()]
print(users)
