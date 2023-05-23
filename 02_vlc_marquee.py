import RPi.GPIO as GPIO
import vlc

BUTTON_PIN = 40

def check_sensor_state():
    # Sensor code goes here.
    # I'm using a push-button with an internal pull-up resistor as an example
    return (GPIO.input(BUTTON_PIN) == GPIO.LOW)

def play_video(player, media):
    # If you don't set the marquee text to an empty string
    # the message will be display at the start of each video.
    # There's probably a better way to fix this!
    player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, "")

    player.set_media(media)
    player.play()

def set_marquee(player, message):
    """ Uses the marquee feature of VLC to display messages over the video"""
    message = message.encode('utf-8')
    player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, message)

def main():
    # GPIO init
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Create a new VLC instance and media player
    instance = vlc.Instance("--sub-source marq")
    player = instance.media_player_new()

    # Font size in pixels (0 for default)
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 0)

    # Message timeout (in ms)
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 1000)

    # Marquee position: 0=center, 1=left, 2=right, 4=top, 8=bottom
    # you can also use combinations of these values, eg 6 = top-right (4 + 2)
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 0)

    # Create libVLC objects representing the two videos
    video1 = vlc.Media("video1.mp4")
    video2 = vlc.Media("video2.mp4")

    # Start the player for the first time
    play_video(player, video1)
    current_video = video1

    # TODO: Add some error handling or at least a proper Ctrl-C handler
    while True:
        # Sensor code goes here
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
            set_marquee(player, "Consider subscribing!")

if __name__ == '__main__':
    main()