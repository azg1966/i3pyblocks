import subprocess
import time

from i3pyblocks import types
from i3pyblocks._internal import subprocess
from i3pyblocks.blocks.base import PollingBlock


class TimerBlock(PollingBlock):

    def __init__(
        self,
        *,
        sleep: int = 1,
        format_time: str = "%M:%S",
        format_stopped: str = "Timer",
        overflow_command: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(sleep=sleep, **kwargs)

        self.compare = 0
        self.format_time = format_time
        self.format_stopped = format_stopped
        self.overflow_command = overflow_command
        self.timer_stopped = True
        self.timer_overflow = False

    async def run(self) -> None:
        if not self.timer_stopped:
            current_time = time.time()
            if current_time >= self.compare:
                if not self.timer_overflow:
                    self.timer_overflow = True
                    await self.on_overflow()
                df = current_time - self.compare
            else:
                df = self.compare - current_time
            full_text = time.strftime(self.format_time, time.gmtime(df))
            self.update(full_text=full_text, urgent=self.timer_overflow)
        else:
            self.update(self.format_stopped)

    async def on_overflow(self):
        command = "i3-msg exec -q {}".format(self.overflow_command)
        subprocess.popener(command)

    def start_timer(self, seconds=300) -> None:
        if self.timer_stopped:
            self.compare = time.time() + seconds
            self.timer_stopped = False
        else:
            self.increase(seconds)

    def stop_timer(self) -> None:
        self.timer_stopped = True
        self.timer_overflow = False
        self.compare = 0

    def increase(self, seconds: int) -> None:
        if not self.timer_stopped and not self.timer_overflow:
            self.compare += seconds

    def decrease(self) -> None:
        if not self.timer_stopped and not self.timer_overflow:
            dif = self.compare - time.time()
            if dif > 60:
                self.compare -= 60

    async def click_handler(self, *, button: int, **kwargs) -> None:
        if button == types.MouseButton.LEFT_BUTTON:
            self.start_timer()
            await self.run()
        elif button == types.MouseButton.SCROLL_UP:
            self.increase(60)
            await self.run()
        elif button == types.MouseButton.SCROLL_DOWN:
            self.decrease()
            await self.run()
        elif button == types.MouseButton.RIGHT_BUTTON:
            self.stop_timer()
            await self.run()
