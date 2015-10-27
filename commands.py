import os
import phue
import voice

# PulseAudio volume sink
SINK = 'alsa_output.pci-0000_00_1b.0.analog-stereo'

# hue strings -> values
HUES = {
	'red': 0,
	'orange': 30,
	'yellow': 60,
	'lime': 90,
	'green': 120,
	'seafoam': 150,
	'foam': 150,
	'cyan': 180,
	'sky': 210,
	'blue': 240,
	'purple': 270,
	'magenta': 300,
	'pink': 330,
}

# number strings -> values
NUMBERS = {
  'one': 1,
  'won': 1,
  'two': 2,
  'to': 2,
  'too': 2,
  '-': 2,
  'three': 3,
  'four': 4,
  'for': 4,
  'five': 5,
  'six': 6,
  'sex': 6,
  'seven': 7,
  'eight': 8,
  'ate': 8,
  'nine': 9,
  'mine': 9,
  'ten': 10,
  'eleven': 11,
  'twelve': 12,
  'thirteen': 13,
  'fourteen': 14,
  'fifteen': 15,
  'sixteen': 16,
  'seventeen': 17,
  'eighteen': 18,
  'nineteen': 19,
  'twenty': 20,
  'twenty-one': 21,
  'twenty one': 21,
  'twenty-two': 22,
  'twenty two': 22,
  'twenty-three': 23,
  'twenty three': 23,
  'twenty-four': 24,
  'twenty four': 24,
  'twenty-five': 25,
  'twenty five': 25,
}

# Hue API
bridge = phue.Bridge('192.168.0.101')
bridge.connect()

# command processing... thing...
handler = voice.Voice()

CONTEXT = None

@handler.command('turn (up|down|on|off) the lights')
@handler.command('turn the lights (up|down|on|off)')
def turn_lights(state, lights=[1, 2, 3]):
  global CONTEXT
  CONTEXT = lights
  if state == 'on':
    bridge.set_light(lights, {'on': True, 'bri': 255})
  elif state == 'off':
    bridge.set_light(lights, {'on': False})
  elif state == 'down':
    bridge.set_light(lights, {'bri': 0})
  elif state == 'up':
    bridge.set_light(lights, {'bri': 255})

@handler.command('make the lights ([A-z]+)')
def make_lights(color, lights=[1, 2, 3]):
  global CONTEXT
  CONTEXT = lights
  if color == 'warm':
    bridge.set_light(lights, {'sat': 64, 'hue': 12700})
  else:
    make_lights_hue(HUES[color], lights)

@handler.command('make the lights (\d+)')
def make_lights_hue(hue, lights=[1, 2, 3]):
  global CONTEXT
  CONTEXT = lights
  hue = int(hue)
  bridge.set_light(lights, {'sat': 255, 'hue': int(hue * 65535 / 360)})

@handler.command('set the lights (?:to|\-) (\w+|\d|\-)')
def set_lights(level, lights=[1, 2, 3]):
  global CONTEXT
  CONTEXT = lights
  if level in NUMBERS:
    level = NUMBERS[level]
  bri = int(int(level) / 9 * 255)
  bridge.set_light(lights, {'bri': bri})

@handler.command('dim the lights')
def dim_lights():
  set_lights(0)


@handler.command('turn (up|down|on|off) all the lights')
@handler.command('turn all the lights (up|down|on|off)')
def turn_all_lights(state):
  turn_lights(state, lights=[1, 2, 3, 4])

@handler.command('make all the lights ([A-z]+)')
def make_all_lights(color):
  make_lights(color, lights=[1, 2, 3, 4])

@handler.command('make all the lights (\d+)')
def make_all_lights_hue(hue):
  make_lights_hue(hue, lights=[1, 2, 3, 4])

@handler.command('set all the lights (?:to|\-) (\w+|\d|\-)')
def set_all_lights(level):
  set_lights(level, lights=[1, 2, 3, 4])

@handler.command('dim all the lights')
def dim_all_lights():
  set_all_lights(0)


@handler.command('turn (up|down|on|off) (?:light|like) (\w+|\d|\-)')
def turn_light(state, index):
  if index in NUMBERS:
    index = NUMBERS[index]
  index = int(index)
  turn_lights(state, lights=index)

@handler.command('make (?:light|like) (\w+|\d|\-) ([A-z]+)')
def make_light(index, color):
  if index in NUMBERS:
    index = NUMBERS[index]
  index = int(index)
  make_lights(color, lights=index)

@handler.command('make (?:light|like) (\w+|\d|\-) (\d+)')
@handler.command('make (?:light|like) (\d)(\d+)')
def make_light_hue(index, hue):
  if index in NUMBERS:
    index = NUMBERS[index]
  index = int(index)
  make_lights_hue(hue, lights=index)

@handler.command('set (?:light|like) (\w+|\d|\-) (?:to|\-) (\w+|\d|\-)')
@handler.command('satellite (\w+|\d|\-) (?:to|\-) (\w+|\d|\-)')
@handler.command('set (?:light|like) (\d)2(\d)')
@handler.command('satellite (\d)2(\d)')
def set_light(index, level):
  if index in NUMBERS:
    index = NUMBERS[index]
  index = int(index)
  set_lights(level, lights=index)

@handler.command('dim light (\w+|\d|\-)')
def dim_light(index):
  set_light(index, 0)


@handler.command('turn (?:them|it) (up|down|on|off)')
def turn_context(state):
  turn_lights(state, lights=CONTEXT)

@handler.command('make (?:them|it) (\w+)')
def make_context(color):
  make_lights(color, lights=CONTEXT)

@handler.command('set (?:them|it) (?:to|\-) (\w+|\d|\-)')
def set_context(level):
  set_lights(level, lights=CONTEXT)

@handler.command('dim (?:them|it)')
def dim_context():
  set_context(0)


@handler.command('lock')
def lock():
  os.system('i3lock -d -c 2e3338')

@handler.command('turn (on|off) monitors')
@handler.command('turn the monitors (on|off)')
@handler.command('turn (on|off) the monitors')
def monitors(state):
  os.system('xset dpms force {}'.format(state))

@handler.command('go to sleep')
def sleep():
  turn_all_lights('off')
  monitors('off')
  set_volume(3)

@handler.command('set the mood')
def mood():
  bridge.set_light(4, {'on': True, 'bri': 64, 'sat': 255, 'hue': 54000})
  bridge.set_light(2, {'on': True, 'bri': 64, 'sat': 255, 'hue': 0})
  bridge.set_light([1, 3], {'on': True, 'bri': 64, 'sat': 255, 'hue': 6000})
  monitors('off')
  set_volume(4)
  next_song()

@handler.command('(?:stop|pause|play|start|turn on|turn off) the music')
def music():
  os.system('xdotool key XF86AudioPlay')

@handler.command('(?:skip|next) song')
def next_song():
  os.system('xdotool key XF86AudioNext')

@handler.command('(?:previous|last) song')
def prev_song():
  os.system('xdotool key XF86AudioPrev')

@handler.command('turn (up|down) the volume')
def volume(state):
  if state == 'up':
    os.system('xdotool key XF86AudioRaiseVolume')
  elif state == 'down':
    os.system('xdotool key XF86AudioLowerVolume')

@handler.command('set the volume to (\d+|\w+)')
def set_volume(val):
  if val in NUMBERS:
    val = NUMBERS[val]

  val = int(val)

  os.system('pactl set-sink-volume {} 0x{:02x}'.format(SINK, val * 2730))


@handler.command('launch ([a-z\.\-]+)')
def launch(handler):
  os.system(handler)

@handler.command('speak (.+)')
def speak(words):
  os.system('espeak "{}"'.format(words))
