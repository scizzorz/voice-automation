import commands

while True:
  cmd = input('> ')
  if cmd == 'thank you':
    break
  commands.handler.process(cmd)
