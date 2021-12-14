---
sidebar_label: handler
title: backend.handler
---

Base handler Spock class

## BaseHandler Objects

```python
class BaseHandler(ABC)
```

Base class for saver and payload

*Attributes*:

    _writers: maps file extension to the correct i/o handler
    _s3_config: optional S3Config object to handle s3 access

