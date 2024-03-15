Frame_rate = 25


class TimeWithFrames:
    def __init__(self, time_string):
        parts = time_string.split(':')
        self.hours = int(parts[0])
        self.minutes = int(parts[1])
        self.seconds = int(parts[2])
        self.frames = int(parts[3])
    def subtract_time(self, other_time):
        total_frames_self = self.total_frames()
        total_frames_other = other_time.total_frames()
        diff_frames = total_frames_self - total_frames_other
        self.hours = diff_frames // (Frame_rate * 3600)
        diff_frames %= (Frame_rate * 3600)
        self.minutes = diff_frames // (Frame_rate * 60)
        diff_frames %= (Frame_rate * 60)
        self.seconds = diff_frames // Frame_rate
        self.frames = diff_frames % Frame_rate


    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}:{self.frames:02d}"

    def total_frames(self):
        total = (self.hours * 3600 + self.minutes * 60 + self.seconds) * Frame_rate + self.frames
        return total

    def add_frames(self, num_frames):
        total_frames = self.total_frames() + num_frames
        self.hours = total_frames // (Frame_rate * 3600)
        total_frames %= (Frame_rate * 3600)
        self.minutes = total_frames // (Frame_rate * 60)
        total_frames %= (Frame_rate * 60)
        self.seconds = total_frames // Frame_rate
        self.frames = total_frames % Frame_rate

    def round_to_seconds(self):
        total_frames = self.total_frames()
        rounded_seconds = total_frames // self.Frame_rate
        self.hours = rounded_seconds // 3600
        rounded_seconds %= 3600
        self.minutes = rounded_seconds // 60
        self.seconds = rounded_seconds % 60
        self.frames = 0