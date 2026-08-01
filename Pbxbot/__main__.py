import asyncio
import traceback

from pyrogram import idle

from Pbxbot import __version__
from Pbxbot.core import (
    Config,
    GachaBotsSetup,
    TemplateSetup,
    UserSetup,
    db,
    Pbxbot,
)
from Pbxbot.functions.tools import initialize_git
from Pbxbot.functions.utility import BList, Flood, TGraph


async def main():
    try:
        print(">>> Starting Pbxbot...")

        await Pbxbot.startup()
        print("✓ Pbxbot started")

        await db.connect()
        print("✓ Database connected")

        await UserSetup()
        print("✓ User setup complete")

        await GachaBotsSetup()
        print("✓ GachaBots setup complete")

        await TemplateSetup()
        print("✓ Template setup complete")

        await Flood.updateFromDB()
        print("✓ Flood updated")

        await BList.updateBlacklists()
        print("✓ Blacklist loaded")

        await TGraph.setup()
        print("✓ Telegraph ready")

        await initialize_git(Config.PLUGINS_REPO)
        print("✓ Plugins repo initialized")

        await Pbxbot.start_message(__version__)
        print("✓ Start message sent")

        print(">>> Bot is now running...")
        await idle()

    except Exception:
        print("\n========== ROOT ERROR ==========")
        traceback.print_exc()
        print("================================\n")
        raise

    finally:
        try:
            await Pbxbot.stop()
        except Exception:
            pass

        try:
            await db.close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
