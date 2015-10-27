import re

class Voice(object):
  def __init__(self):
    self.routes = []

  def process(self, phrase):
    for route in self.routes:
      route.process(phrase)

  def command(self, path):
    def wrapper(func):
      if isinstance(func, Route):
        func.add_path(path)
      else:
        func = Route(path, func)
        self.routes.append(func)
      return func
    return wrapper

class Route(object):
  def __init__(self, path, func):
    self.paths = [re.compile(path)]
    self.func = func

  def add_path(self, path):
    self.paths.append(re.compile(path))

  def __call__(self, *args, **kwargs):
    self.func(*args, **kwargs)

  def process(self, phrase):
    for path in self.paths:
      res = path.search(phrase)
      if res is not None:
        print(path.pattern, "::", *res.groups())
        self.func(*res.groups())
