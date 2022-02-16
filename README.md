<img src="https://cdn.discordapp.com/attachments/857979752991031296/943164374510600284/radish3.svg" alt="Radish" align="right" style="width: 350px;"/>
<h1>Radish </h1>

<p>Radish is a simple router implementation for my web framework, <a href="https://github.com/cheetahbyte/ermine">Ermine</a>. However, it can also be used for other things, and provides complete typing. It does use an regex tree for routing.</p>

## 🔑 Key Features
- simple
- elegant
- comprehensiv


## Quick example

<img src="https://cdn.discordapp.com/attachments/826113544021082143/943460509804527686/unknown.png" style="width: 350px;"/>


## ⬇️ Installation
<br>

> pip install radish-router

## 🤔 Inspiration
Radish is inspired by:
- https://github.com/klen/http-router
- https://github.com/nekonoshiri/tiny-router

## 🌟 Features: 
- [x] simple matching
- [x] dynamic routes
- [x] parameters
- [x] wildcards
- [x] radix trees

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

router.insert("get", "/user/:uid", handler)

router.insert("get", "/static/*filename", handler)

print(router.get("get", "/user/16e55f79-baa7-46ed-b9a8-8dabc35c6381"))

print(router.get("get", "/hello/world"))
```
---
*¹ Remember that method, handler and params are reserved keywords. You can use any other keyword.