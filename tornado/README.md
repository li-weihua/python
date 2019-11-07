## sending binary file to client (not for big file)

```python
 with open(path, 'rb') as f:
      data = f.read()
      self.write(data)
  self.finish()
```

