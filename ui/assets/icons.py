import framebuf

from config import Icons as IconConfig, ScreenId

# One byte per row, MSB = leftmost pixel
_HEART = bytearray([0x66, 0xFF, 0xFF, 0x7E, 0x3C, 0x18, 0x00, 0x00])
_BARS = bytearray([0x00, 0x18, 0x18, 0x1B, 0xDB, 0xDB, 0xDB, 0xDB])
_CLOUD = bytearray([0x00, 0x1C, 0x3E, 0x7F, 0xFF, 0xFF, 0x7E, 0x00])
_CLOCK = bytearray([0x3C, 0x42, 0x89, 0x89, 0x8D, 0x81, 0x42, 0x3C])


class MenuIcons:
    """8x8 menu icons as framebuffers, looked up by ScreenId."""

    def __init__(self):
        self._by_screen = {
            ScreenId.HEART_RATE: self._make(_HEART),
            ScreenId.HRV: self._make(_BARS),
            ScreenId.KUBIOS: self._make(_CLOUD),
            ScreenId.HISTORY: self._make(_CLOCK),
        }

    def for_screen(self, screen_id):
        return self._by_screen[screen_id]

    @staticmethod
    def _make(data):
        return framebuf.FrameBuffer(data, IconConfig.SIZE, IconConfig.SIZE,
                                    framebuf.MONO_HLSB)