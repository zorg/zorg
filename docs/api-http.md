# How to connect with the HTTP API

Zorg comes with built-in HTTP API support to allow you to interact with your robots remotely.

# Running your robot

The following example code demonstrates how to spin up an API server.

```python
import zorg

robot = zorg.robot({
    "name": "test_robot",
    "connections": {},
    "devices": {},
    "work": None,
})

api = zorg.api("zorg.api.Http", {})

robot.start()
api.start()
```

By default, an unconfigured API instance will listen on `http://127.0.0.1:8000`.

For more information API configuration, see the [configuration page](configuration.md).

For more information on available API routes, check out the [CPPP-IO](http://cppp.io/) spec that Zorg's API follows.
