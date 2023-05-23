import RPi.GPIO as GPIO
import vlc

# This is a very basic example program to display two videos
# in loop using python-vlc on a Raspberry Pi

# Performance is not *perfect* but the code is very easy to use
# and customize, sound playback is working and the player
# will work with virtually any file type (even images or just sound)

# Using OOP would be a good idea to hide everything related to VLC
# and video playback but I tried to keep this code short and easy to re-use

BUTTON_PIN = 40

def check_sensor_state():
    # Sensor code goes here.
    # I'm using a push-button with an internal pull-up resistor as an example

    return (GPIO.input(BUTTON_PIN) == GPIO.LOW)

def play_video(player, media):
    # You need to call "set_media()" to (re)load a video before playing it

    player.set_media(media)
    player.play()

def main():
    # GPIO init

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Create a new VLC instance and media player:
    #
    # This could be done in one line using vlc.MediaPlayer()
    # that will create an instance behind the scene
    # but we will pass some parameters to the instance in future example codes

    instance = vlc.Instance()
    player = instance.media_player_new()

    # Create libVLC objects representing the two videos
    video1 = vlc.Media("video1.mp4")
    video2 = vlc.Media("video2.mp4")

    # Start the player for the first time
    play_video(player, video1)
    current_video = video1

    # TODO: Add some error handling or at least a proper Ctrl-C handler
    while True:
        triggered = check_sensor_state()

        # Swap video if needed
        if triggered and current_video == video1:
            play_video(player, video2)
            current_video = video2
        elif not triggered and current_video == video2:
            play_video(player, video1)
            current_video = video1

        # Loop video if playback is ended
        if player.get_state() == vlc.State.Ended:
            play_video(player, current_video)

if __name__ == '__main__':
    main()