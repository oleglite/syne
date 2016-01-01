import argh
import pickle
import pyaudio
import random
import sys
import time


PICKLE_PROTOCOL = 3


def log(msg):
    print(msg)


def chunks(arr, size):
    """
    >>> for chunk in chunks([1,2,3,4,5], 2): print(chunk)
    [1, 2]
    [3, 4]
    [5]
    """
    for i in range(0, len(arr), size):
        yield arr[i:i + size]


class Sound(object):
    def __init__(self):
        self.chunk_size = 1000
        self.format = pyaudio.paInt8
        self.channels = 1
        self.rate = 16000
        self.record_seconds = 5
        self.frames = b''

        self.time_for_symbol = 1
        self.symbols_in_session = 10
        self.alphabet = ['1', '_']
        self.symbols = ''

        self._pyaudio_obj = None
        self._stream = None

    def set_data(self, data):
        audio = data['audio']
        self.format = audio['format']
        self.channels = audio['channels']
        self.rate = audio['rate']
        self.frames = audio['frames']

        text = data['text']
        self.time_for_symbol = text['time_for_symbol']
        self.symbols = text['symbols']

    def get_data(self):
        data = {
            'audio': {
                'format': self.format,
                'channels': self.channels,
                'rate': self.rate,
                'frames': self.frames
            },
            'text': {
                'time_for_symbol': self.time_for_symbol,
                'symbols': self.symbols
            }
        }
        return data

    def clear(self):
        self.symbols = ''
        self.frames = b''

    def record(self):
        self._open_stream(input=True)
        log("* recording")

        frames = []
        symbols = self._generate_symbols()

        for symbol in symbols:
            self._show_symbol(symbol)

            for i in range(0, int(self.rate / self.chunk_size * self.time_for_symbol)):
                chunk = self._stream.read(self.chunk_size)
                frames.append(chunk)

        self._close_stream()
        log("\n* done recording")

        self.frames += b''.join(frames)
        self.symbols += symbols

    def play(self):
        self._open_stream(output=True)

        symbols_frames = chunks(self.frames, self.rate * self.time_for_symbol * self._frame_size())

        for symbol, symbol_frames in zip(self.symbols, symbols_frames):
            self._show_symbol(symbol)

            for chunk in chunks(symbol_frames, self.chunk_size * self._frame_size()):
                self._stream.write(chunk)

        self._close_stream()

    def _open_stream(self, input=False, output=False):
        assert not self._pyaudio_obj
        assert not self._stream

        self._pyaudio_obj = pyaudio.PyAudio()

        time.sleep(1)

        self._stream = self._pyaudio_obj.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=self.chunk_size,
            input=input,
            output=output,
        )

    def _close_stream(self):
        assert self._pyaudio_obj
        assert self._stream
        self._stream.stop_stream()
        self._stream.close()
        self._pyaudio_obj.terminate()

    def _show_symbol(self, symbol):
        sys.stdout.write(symbol)
        sys.stdout.flush()

    def _frame_size(self):
        return self._pyaudio_obj.get_sample_size(self.format)

    def _generate_symbols(self):
        return ''.join(random.choice(self.alphabet) for _ in range(self.symbols_in_session))


def record():
    sound = Sound()
    sound.record()
    data = sound.get_data()
    with open('output', 'wb') as f:
        pickle.dump(data, f, protocol=PICKLE_PROTOCOL)


def play():
    with open('../output', 'rb') as f:
        data = pickle.load(f)
    sound = Sound()
    sound.set_data(data)
    sound.play()
    print(len(data['audio']['frames']))


if __name__ == '__main__':
    argh.dispatch_commands([record, play])

