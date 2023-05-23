import vlc


class VLCMediaPlayer():
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.current_video = None

    def load_videos(self, path_not_triggered, path_triggered):
        self.normal_vid = vlc.Media(path_not_triggered)
        self.trigger_vid = vlc.Media(path_triggered)

        # This is supposed to "pre-parse" the videos before playing it.
        # The performance improvement is very low but that doesn't hurt!
        self.normal_vid.parse()
        self.trigger_vid.parse()

    def play_video(self, media):
        # You need to call "set_media()" to (re)load a video before playing it
        self.player.set_media(media)
        self.player.play()
        self.current_video = media

    def update(self, triggered):
        current_video = self.get_current_video()

        # Change video if needed
        if triggered and current_video == self.normal_vid:
            self.play_video(trigger_vid)
        elif not triggered and current_video == self.trigger_vid:
            self.play_video(normal_vid)

        # Loop video if playback is ended
        if self.is_ended():
            self.play_video(current_video)

    def get_current_video(self):
        return self.current_video

    def is_ended(self):
        return (self.player.get_state() == vlc.State.Ended)
        
def main():
    player = VLCMediaPlayer()

    player.load_videos("video1.mp4", "video2.mp4")

    while True:
        # Sensor code goes here
        triggered = check_sensor_state()
        player.update()

if __name__ == '__main__':
    main()