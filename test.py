from radish.radish import Radish

radish = Radish()


radish.insert("GET", "/user/:id/:abc", lambda: "dynamic")
radish.insert("GET", "/user/:id/*file", lambda: "lol")
# radish.insert("GET", "/user/static/*file", lambda: "root")
# print(radish.get("GET", "/user/abc/file"))
