import asyncio
from playwright.async_api import async_playwright

APP_URLS = [
    "https://autoinsight-26.streamlit.app",   # <-- replace with app 1
    "https://pharmainsight.streamlit.app",  # <-- replace with app 2
]

async def wake_app(page, url):
    print(f"Visiting {url} ...")
    await page.goto(url, timeout=60000)
    await page.wait_for_timeout(8000)  # stay a bit so Streamlit registers a real session

    try:
        button = page.get_by_text("Yes, get this app back up!", exact=False)
        if await button.is_visible(timeout=3000):
            await button.click()
            print(f"{url} was asleep — clicked wake button.")
            await page.wait_for_timeout(15000)
    except Exception:
        print(f"{url} was already awake.")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for url in APP_URLS:
            await wake_app(page, url)
        await browser.close()
        print("Done with all apps.")

asyncio.run(main())
