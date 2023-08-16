import aiohttp
from fpl import FPL

async def getGameWeeks():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        gameweeks = await fpl.get_gameweeks()

    return gameweeks