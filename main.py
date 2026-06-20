import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("binarium-webapp-bot")

BASE_DIR = Path(__file__).resolve().parent
WEBAPP_DIR = BASE_DIR

BOT_TOKEN = os.getenv("BOT_TOKEN", "8794195724:AAH_JSB_LUsdUEu-cWhtxSaUsGBpuwntXlY").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()
RAILWAY_PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
PORT = int(os.getenv("PORT", "8000"))

if not WEBAPP_URL and RAILWAY_PUBLIC_DOMAIN:
    WEBAPP_URL = f"https://{RAILWAY_PUBLIC_DOMAIN}"

app = FastAPI(title="Binarium AI Terminal")
app.mount("/static", StaticFiles(directory=str(WEBAPP_DIR)), name="static")

@app.get("/")
async def webapp_index():
    return FileResponse(WEBAPP_DIR / "index.html")

@app.get("/health")
async def health():
    return {"ok": True}

bot: Bot | None = None
dp: Dispatcher | None = None

async def make_start_keyboard() -> InlineKeyboardMarkup:
    if WEBAPP_URL:
        btn = InlineKeyboardButton(text="🚀 Відкрити термінал", web_app=WebAppInfo(url=WEBAPP_URL))
    else:
        btn = InlineKeyboardButton(text="⚠️ WEBAPP_URL не заданий", callback_data="no_url")
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])

async def register_handlers(dispatcher: Dispatcher):
    @dispatcher.message(CommandStart())
    async def start(message: Message):
        kb = await make_start_keyboard()
        await message.answer(
            "🚀 <b>BINARIUM AI TERMINAL</b>\n\n"
            "Преміум WebApp-термінал сигналів Binarium.\n"
            "Натисни кнопку нижче, щоб відкрити термінал.",
            reply_markup=kb,
            parse_mode="HTML",
        )

    @dispatcher.message(F.text)
    async def any_text(message: Message):
        kb = await make_start_keyboard()
        await message.answer("👇 Відкрий термінал кнопкою нижче:", reply_markup=kb)

async def bot_runner():
    global bot, dp
    if not BOT_TOKEN:
        log.warning("BOT_TOKEN is empty. FastAPI is running, bot is disabled.")
        return
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    await register_handlers(dp)
    log.info("Starting Telegram bot polling")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(bot_runner())

@app.on_event("shutdown")
async def on_shutdown():
    if bot:
        await bot.session.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
