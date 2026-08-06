import os
import asyncio
import traceback
from threading import Thread
from flask import Flask
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

# ==================== FLASK KEEP-ALIVE SETUP ====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Pbxbot is alive and running fine!"

def run_flask():
    # Render se PORT pick karega (default 8080)
    port = int(os.environ.get("PORT", 8080))
    
    # Extra Flask logs hide karne ke liye
    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    server_thread = Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
    print("✓ Flask Keep-Alive Server Started")
# ================================================================


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
    # Bot start hone se pehle Flask server background me chalu hoga
    keep_alive()
    asyncio.run(main())
