# tornado server examples

## send image to server by base64

- client
[client.py](./post_image/client.py)

- server
[server.py](./post_image/server.py)


## sending binary file to client (not for big file)

```python
 with open(path, 'rb') as f:
      data = f.read()
      self.write(data)
  self.finish()
```

