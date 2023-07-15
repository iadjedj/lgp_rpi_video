# Le Grille-Pain
## How to Build a Gapless Video Player on a Raspberry Pi

Example codes for [my video](https://www.youtube.com/watch?v=Y3SJ8qLqQA8) about seamless video playback on a Raspberry Pi

## Instructions

### Usual stuff

Install Raspberry Pi OS, configure Wi-Fi and update your install :

```bash
sudo raspi-config # configure Wi-Fi
sudo apt update && sudo apt upgrade

```

### For the VLC version

```bash
sudo apt install pip
pip install python-vlc
```
Code was tested with VLC 3.0.18 and python_vlc 3.0.18121

### For the openCV version

Install opencv with ```pip install python3-opencv```

### Force a WQHD (2K) framebuffer

Add in `/boot/config.txt` (this will overclock the GPU, do it at **your own risks**) :

```
hdmi_group=2
hdmi_mode=87
hdmi_cvt=2560 1440 60 3 0 0 1
max_framebuffer_width=2560
max_framebuffer_height=1440
hdmi_pixel_freq_limit=400000000
```
