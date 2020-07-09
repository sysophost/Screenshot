import logging

import pyppeteer
from pyppeteer import launch


class pyShot(object):
    def __init__(self, proxy=None):
        self.proxy = proxy

    async def capture_screenshot(self, browser: pyppeteer.browser, url: str):
        filename = url
        for r in (("://", "_"), ("/", "_"), (":", "_")):
            filename = filename.replace(*r)

        page = await browser.newPage()

        try:
            logging.info(f"[i] Capturing screenshot of {url}")
            await page.goto(url)
            await page.screenshot({'path': f'{filename}.png'})
        except Exception:
            logging.error(f"[!] Something went wrong when accessing {url}")

    async def get_browser(self) -> pyppeteer.browser:
        browser_args = pyppeteer.defaultArgs()
        if self.proxy:
            browser_args.append(f"--proxy-server={self.proxy}")
            logging.info(f"[i] Using proxy {self.proxy}")
        browser = await launch({'ignoreHTTPSErrors': True, 'defaultViewport': {'width': 1280, 'height': 1024}}, args=browser_args)

        return browser
