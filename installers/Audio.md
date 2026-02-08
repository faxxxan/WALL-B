# I2S Audio Configuration Summary (Reference)

All the configuration is based on two scripts from Adafruit, which in turn were based on scripts from Pimoroni.
https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/

- i2samp.py : Installer script for I2S audio devices.
- i2smic.py : Installer script for I2S microphone devices.

In addition, there is configuration needed to allow speech recognition to work with the microphone.

The Adafruit scripts were recently moved from shell scripts to Python scripts, however I also have my own shell scripts in the `installers/` folder which are based on their original shell scripts.

In 2025 I had to configure audio on the CM5 carrier board. This was partially successful but I needed to restart and occasionally re-run the i2samp.py script to get audio working again.

As far as I know there are no differences between the Raspberry Pi 5 and CM5 in terms of audio configuration.

Unfortunately, when testing recently I can't get this to work at all on the CM5. The devices are detected but I have not managed to get them to record or play audio.

Below is the dump of my investigation around the configuration files needed, and the ideal contents of those files. Despite this I have not managed to resolve the issues on the CM5.

## 1. Device Tree and Overlays
- Only one I2S audio overlay should be enabled in `/boot/firmware/config.txt` (or `/boot/config.txt`).
- For the Google Voice HAT, use:
	```
	dtoverlay=googlevoicehat-soundcard
	```
- Disable onboard audio to avoid conflicts:
	```
	#dtparam=audio=on
	```
- To prevent HDMI audio devices from appearing and changing card numbers, add:
	```
	hdmi_ignore_edid_audio=1
	```
- Comment out or remove any other I2S overlays (e.g., `max98357a`, `dual_i2s`, `i2s-mmap`).

**Example [all] section:**
```
[all]
dtparam=uart0=on
dtoverlay=googlevoicehat-soundcard
hdmi_ignore_edid_audio=1
#dtparam=audio=on # this may be added elsewhere; ensure it's disabled
```

## 2. Blacklist File
- `/etc/modprobe.d/raspi-blacklist.conf` is usually empty or does not exist by default.
- If present, ensure any lines blacklisting I2S drivers are commented out (start with `#`).

## 3. ALSA Configuration (`/etc/asound.conf`)
- This file defines the software audio pipeline for playback.
- For I2S output, use:
	```
	pcm.speakerbonnet {
		 type hw card 0
	}

	pcm.dmixer {
		 type dmix
		 ipc_key 1024
		 ipc_perm 0666
		 slave {
			 pcm "speakerbonnet"
			 period_time 0
			 period_size 1024
			 buffer_size 8192
			 rate 44100
			 channels 2
		 }
	}

	ctl.dmixer {
			type hw card 0
	}

	pcm.softvol {
			type softvol
			slave.pcm "dmixer"
			control.name "PCM"
			control.card 0
	}

	ctl.softvol {
			type hw card 0
	}

	pcm.!default {
			type             plug
			slave.pcm       "softvol"
	}
	```
- This sets the default output to use software volume and mixing, targeting card 0 (your I2S device).

## 4. Systemd Service (`/etc/systemd/system/aplay.service`)
- Keeps the audio device open to prevent popping/clicking:
	```
	[Unit]
	Description=Invoke aplay from /dev/zero at system start.

	[Service]
	ExecStart=/usr/bin/aplay -D default -t raw -r 44100 -c 2 -f S16_LE /dev/zero

	[Install]
	WantedBy=multi-user.target
	```
- Enable only if needed.

## 5. Testing Audio
- Use the default device for playback:
	```
	speaker-test -D default -c2 -t wav -r 44100
	```
- Or play a WAV file:
	```
	aplay -D default /usr/share/sounds/alsa/Front_Center.wav
	```
- Ignore warnings about sample rate mismatch if you hear sound; ALSA is resampling.

## 6. Microphone/Input Devices
- asound.conf does not define input devices.
- Use `arecord -l` to list capture devices.
- Use `arecord` to test recording:
	```
	arecord -D hw:0,0 -f S16_LE -c 1 -r 16000 test.wav
	```
- For speech_recognition, use:
	```python
	import speech_recognition as sr
	print(sr.Microphone.list_microphone_names())
	```
	and select the correct device by name or index.

## 7. Common Issues and Solutions
- **No sound:** Check card number in asound.conf matches your I2S device (use `aplay -l`).
- **Playback errors with hw:0,0:** Use `default` or `plughw:0,0` for format conversion.
- **HDMI devices present:** Add `hdmi_ignore_edid_audio=1` and comment out `dtoverlay=vc4-kms-v3d` if not needed.
- **Multiple overlays:** Only enable the one matching your hardware.
- **No input device:** Ensure your mic is detected by ALSA and appears in `arecord -l` and `sr.Microphone.list_microphone_names()`.

## 8. Summary Table of Key Files

| File/Setting                | Ideal Content/Setting                                                                 |
|-----------------------------|--------------------------------------------------------------------------------------|
| /boot/firmware/config.txt   | Only `dtoverlay=googlevoicehat-soundcard` enabled, `dtparam=audio=on` disabled       |
| /etc/modprobe.d/raspi-blacklist.conf | Empty or all lines commented out                                            |
| /etc/asound.conf            | As above, with card number matching your I2S device                                 |
| /etc/systemd/system/aplay.service | As above, optional                                                            |
| arecord -l / aplay -l       | Confirm card 0 is your I2S device                                                   |
| speech_recognition devices  | Use `sr.Microphone.list_microphone_names()` to find the correct input device         |

## 9. General Best Practices
- Always match card numbers in asound.conf to your actual hardware.
- Only enable one I2S overlay at a time.
- Use ALSA’s default or plug devices for best compatibility.
- Use arecord and aplay for basic input/output testing.
- Use speech_recognition’s device listing to select the correct mic.



# Terms and Definitions
## Device Tree
A data structure used by the Linux kernel to describe the hardware layout of a system (especially on ARM devices like Raspberry Pi).
The device tree tells the kernel what hardware is present and how to configure it (e.g., enabling I2S audio via overlays like dtoverlay=googlevoicehat-soundcard).
Overlays are small snippets that add or modify device tree entries at boot, enabling specific hardware features.

## Blacklist File
A configuration file (e.g., /etc/modprobe.d/raspi-blacklist.conf) used to prevent certain kernel modules (drivers) from loading automatically.
By "blacklisting" a module, you stop the kernel from loading it at boot, which can be necessary to avoid conflicts or disable unused hardware.
Commenting out lines in this file (adding #) re-enables the module.

[This is an empty file in my pi]

## ALSA (Advanced Linux Sound Architecture)
The main sound system in Linux for handling audio devices, drivers, and sound mixing.
Provides low-level audio device access and configuration via files like /etc/asound.conf.
Applications use ALSA to play, record, and process audio.

## dmix
An ALSA plugin that allows multiple applications to play audio at the same time on hardware that does not support hardware mixing.
Without dmix, only one application could use the sound device at a time.
dmix mixes multiple audio streams in software and sends the result to the hardware.

## softvol
An ALSA plugin that provides software-based volume control.
Useful for hardware that lacks its own volume control (like many I2S amplifiers).
Allows you to adjust the output volume in software, regardless of hardware capabilities.

## i2samp.py
A Python installer script designed to set up I2S audio on a Raspberry Pi.
Automates tasks like enabling device tree overlays, configuring ALSA, and testing audio output.
It modifies system files, installs necessary packages, and ensures the I2S audio device is properly configured.

## /boot/firmware/config.txt

dtparam=audio=on enables the onboard audio (snd_bcm2835). If you are using an external I2S amplifier, you may want to disable this to avoid conflicts

only `dtoverlay=googlevoicehat-soundcard` is needed to enable the I2S audio device for the Google Voice HAT. Other overlays like `i2s-mmap`, `max98357a`, or `dual_i2s` are not necessary and may cause conflicts.


