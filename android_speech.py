"""Android Mandarin audio playback, with no Python<->Java TTS callbacks.

The Android TextToSpeech listener lives entirely in SpeechBridge.java to avoid
PythonJavaClass callbacks on Java-owned threads. Failures are surfaced by Android
Toast instead of causing exceptions in Kivy's UI callbacks.
"""

from kivy.utils import platform


class MandarinSpeech:
    def __init__(self, report):
        self.report = report
        self.closed = False
        if platform != 'android':
            self._activity = None
            self._bridge = None
            return
        from jnius import autoclass
        self._activity = autoclass('org.kivy.android.PythonActivity').mActivity
        self._bridge = autoclass('vn.hoctiengtrung.SpeechBridge')

    def play(self, text):
        if self.closed or not text:
            return
        if self._bridge is None:
            self.report('Phát âm tiếng Trung chỉ hỗ trợ trên Android.')
            return
        self._bridge.play(self._activity, str(text))

    def stop(self):
        if not self.closed and self._bridge is not None:
            self._bridge.stop(self._activity)

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self._bridge is not None:
            self._bridge.shutdown(self._activity)
