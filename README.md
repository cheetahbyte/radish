<img src="https://cdn.discordapp.com/attachments/857979752991031296/943164374510600284/radish3.svg" alt="Radish" align="right" style="width: 350px;"/>
<h1>Radish </h1>

<p>Radish is a simple router implementation for my web framework, <a href="https://github.com/cheetahbyte/ermine">Ermine</a>. However, it can also be used for other things, and provides complete typing. It does not use radix trees, but can be used with regex.</p>

Radish is inspired by:
- https://github.com/klen/http-router
- https://github.com/nekonoshiri/tiny-router

- simple
- elegant
- comprehensiv


## Features: 
- [ ] regex matching
- [x] simple matching
- [ ] dynamic routes
- [ ] parameters

## Examples

> Basic static route matching

```py
from radish import Radish

router = Radish()

def handler1():
    return "Hello World!"

router.insert("get", "/hello/world", handler1) # You can pass in any keyword argument . *¹

print(router.get("post", "/hello/world"))
# will return  
# {"route": "/user","handler": handler2, "params": {}}
```

---
*¹ Remember that method, handler and params are reserved keywords. 
