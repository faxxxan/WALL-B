
<<<<<<< Updated upstream
sudo myenv/bin/python3 -m pip install --upgrade click

sudo myenv/bin/python3 -m pip install --upgrade setuptools
sudo myenv/bin/python3 -m pip install --upgrade adafruit-python-shell

sudo myenv/bin/python3 installers/i2samp.py
=======
sudo python3 -m pip install --upgrade click --break-system-packages

sudo python3 -m pip install --upgrade setuptools --break-system-packages
sudo python3 -m pip install --upgrade adafruit-python-shell --break-system-packages

sudo python3 installers/i2samp.py

# cm5@cm5:~/modular-biped $ aplay -l
# **** List of PLAYBACK Hardware Devices ****
# card 0: vc4hdmi0 [vc4-hdmi-0], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0
# card 1: vc4hdmi1 [vc4-hdmi-1], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0
# card 2: I2S [Dual I2S], device 0: 1f000a0000.i2s-dit-hifi dit-hifi-0 [1f000a0000.i2s-dit-hifi dit-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0

# RESTART

# **** List of PLAYBACK Hardware Devices ****
# card 0: vc4hdmi0 [vc4-hdmi-0], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0
# card 1: vc4hdmi1 [vc4-hdmi-1], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0
# card 2: sndrpigooglevoi [snd_rpi_googlevoicehat_soundcar], device 0: Google voiceHAT SoundCard HiFi voicehat-hifi-0 [Google voiceHAT SoundCard HiFi voicehat-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0

# RESTART

# **** List of PLAYBACK Hardware Devices ****
# card 0: vc4hdmi0 [vc4-hdmi-0], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0
# card 1: sndrpigooglevoi [snd_rpi_googlevoicehat_soundcar], device 0: Google voiceHAT SoundCard HiFi voicehat-hifi-0 [Google voiceHAT SoundCard HiFi voicehat-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0
# card 2: vc4hdmi1 [vc4-hdmi-1], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
#   Subdevices: 1/1
#   Subdevice #0: subdevice #0

>>>>>>> Stashed changes
