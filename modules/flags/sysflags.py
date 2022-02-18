from typing import Optional

from disnake.ext import commands


class BasicFlags(commands.FlagConverter, prefix="-", delimiter='='):
    test: Optional[str]
    cringe: Optional[str]
    based: Optional[str]
