"""Blocks that does not have any extra dependency except i3pyblock itself."""

from i3pyblocks import blocks, types
import subprocess
import asyncio


class TextBlock(blocks.Block):
    r"""Block that shows arbitrary text in i3pyblocks.

    :param full_text:
        Text to be shown.

    :param \*\*kwargs: Arguments to be passed to
        :meth:`i3pyblocks.blocks.base.Block.update_state()` method.
    """

    def __init__(self, full_text: str, **kwargs) -> None:
        super().__init__(block_name=kwargs.pop("block_name", None))
        super().update_state(full_text=full_text, **kwargs)

    async def start(self) -> None:
        self.push_update()


class LauncherBlock(TextBlock):
    def __init__(self, full_text: str, command: str, **kwargs) -> None:
        super().__init__(full_text, **kwargs)
        self.command = command

    async def click_handler(
        self,
        *,
        x: int,
        y: int,
        button: int,
        relative_x: int,
        relative_y: int,
        width: int,
        height: int,
        modifiers: list[str | None]
    ) -> None:
        if button == types.MouseButton.LEFT_BUTTON:
            await asyncio.create_subprocess_shell(
                self.command,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                start_new_session=True
            )
