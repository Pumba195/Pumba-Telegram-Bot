import asyncio
from io import BytesIO
from playwright.async_api import async_playwright
from PIL import Image

from config.config import bot

class AlertScreenshotter:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._page = None
        self._lock = asyncio.Lock()
        self._ready = False

    async def _init_browser(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch()
        self._page = await self._browser.new_page()

        await self._page.goto("https://alerts.in.ua/")
        await self._page.wait_for_selector('div.screenshot-make')

        try:
            await self._page.wait_for_selector('i.fa-moon', timeout=5000)
            await self._page.click('i.fa-moon')
        except Exception:
            try:
                await self._page.wait_for_selector('button:has-text("Тема")', timeout=5000)
                await self._page.click('button:has-text("Тема")')
            except Exception:
                pass

        self._ready = True

    async def get_png_bytes(self) -> bytes:
        async with self._lock:
            if not self._ready:
                await self._init_browser()

            await self._page.reload()
            await self._page.wait_for_selector('div.screenshot-make')

            async with self._page.expect_download() as download_info:
                await self._page.click('div.screenshot-make')

            download = await download_info.value
            path = await download.path()

            with open(path, 'rb') as f:
                return f.read()

    async def close(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()