class GlobalStore:

  def __init__(self):
    self.store = {}

  def add(self, key, content, update_method='append'):
    if update_method == 'replace':
      self.store[key] = content
    elif update_method == 'append':
      previous = self.store.get(key, [])
      self.store[key] = previous + content
    else:
      print("Update method not supported : ", update_method)

  def get(self, key):
    return self.store.get(key)

  def pop(self, key):
    return self.store.pop(key, None)

  def delete(self, key):
    return self.store.pop(key, None)
