import logging
from datetime import datetime

import pyppeteer
from pyppeteer import launch


class pyShot(object):
    def __init__(self, proxy=None, outputdir='.'):
        self.proxy = proxy
        self.outputdir = outputdir

    async def capture_screenshot(self, browser: pyppeteer.browser, url: str):
        filename = url
        for r in (("://", "_"), ("/", "_"), (":", "_")):
            filename = filename.replace(*r)

        timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        filename = filename + f"__{timestamp}"

        page = await browser.newPage()

        try:
            logging.info(f"[i] Capturing screenshot of {url}")
            await page.goto(url)
            await page.screenshot({'path': f'{self.outputdir}/{filename}.png'})
        except Exception:
            logging.error(f"[!] Something went wrong when accessing {url}")

    async def get_browser(self) -> pyppeteer.browser:
        browser_args = pyppeteer.defaultArgs()
        if self.proxy:
            browser_args.append(f"--proxy-server={self.proxy}")
            logging.info(f"[i] Using proxy {self.proxy}")
        browser = await launch({'ignoreHTTPSErrors': True, 'defaultViewport': {'width': 1280, 'height': 1024}}, args=browser_args)

        return browser
