<img src="https://cdn.discordapp.com/attachments/857979752991031296/943164374510600284/radish3.svg" alt="Radish" align="right" style="width: 350px;"/>
<h1>Radish </h1>

<p>Radish is a simple router implementation for my web framework, <a href="https://github.com/cheetahbyte/ermine">Ermine</a>. However, it can also be used for other things, and provides complete typing. It does not use radix trees, but can be used with regex.</p>

## 🔑 Key Features
- simple
- elegant
- comprehensiv


## Quick example

<img src="https://cdn.discordapp.com/attachments/826113544021082143/943460509804527686/unknown.png"/>


## ⬇️ Installation
<br>

> pip install radish-router

## 🤔 Inspiration
Radish is inspired by:
- https://github.com/klen/http-router
- https://github.com/nekonoshiri/tiny-router

## 🌟 Features: 
- [ ] regex matching
- [x] simple matching
- [ ] dynamic routes
- [ ] parameters

## 🔭 Examples

> Basic static route matching

```py
from radish import Radish

router = Radish()

handler = lambda: "Hello World!"

router.insert("get", "/hello/world", handler) # You can pass in any keyword argument . *¹

print(router.get("get", "/hello/world"))
# will return  
# {"route": "/user","handler": handler, "params": {}}
```

> Route parameters


```py
from radish import Radish

route =  Radish()

handler = lambda: "Hello World!"

router.insert("get", "/hello/:name", handler)

router.insert("get", "/user/:uid|uuid", handler) # converters *²

router.insert("get", "/static/*filename", handler)

print(router.get("get", "/user/16e55f79-baa7-46ed-b9a8-8dabc35c6381"))
# will return
# {"route": "/user/:uid","handler": handler, "params": {"uid": UUID("16e55f79-baa7-46ed-b9a8-8dabc35c6381")}}

print(router.get("get", "/hello/world"))
# will return
# {"route": "/hello/world","handler": handler1, "params": {"name": "world"}}
```
---
*¹ Remember that method, handler and params are reserved keywords. 
*² `|type` is used to convert the given parameter to the type. Availble types: `int`, `float`, `str`, `uuid`