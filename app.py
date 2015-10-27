import flask
import commands

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  if path == 'favicon.ico':
    return
  print('Received: {}'.format(path))
  commands.handler.process(path)
  return 'Handling command: {}'.format(path)

if __name__ == '__main__':
  app.run(host='0.0.0.0')

