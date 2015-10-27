# voice-automation

A thing for handling home automation voice commands.

I have a [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en) task that asks for voice input and forwards it via HTTP to a the [app.py](https://github.com/scizzorz/voice-automation/blob/master/app.py) Flask server on my network. The [commands.py](https://github.com/scizzorz/voice-automation/blob/master/commands.py) file does the actual processing, so it's possible to use it with any "input" method.
