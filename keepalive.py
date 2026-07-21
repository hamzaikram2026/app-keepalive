import asyncio
from playwright.async_api import async_playwright

APP_URLS = [
    "https://autoinsight-26.streamlit.app",   # <-- app 1
    "https://pharmainsight.streamlit.app",    # <-- app 2
]


async def wake_app(browser, url):
    print(f"Visiting {url} ...")
    page = await browser.new_page()
    try:
        await page.goto(url, timeout=60000)
        # Give Streamlit time to load and register a real session
        await page.wait_for_timeout(8000)

        try:
            button = page.get_by_text("Yes, get this app back up!", exact=False)
            await button.wait_for(state="visible", timeout=5000)
            await button.click()
            print(f"{url} was asleep — clicked wake button.")
            # Wait for the app to finish waking up
            await page.wait_for_timeout(15000)
        except Exception:
            print(f"{url} was already awake.")

    except Exception as e:
        print(f"Failed to load {url}: {e}")

    finally:
        await page.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for url in APP_URLS:
            await wake_app(browser, url)
        await browser.close()
        print("Done with all apps.")


if __name__ == "__main__":
    asyncio.run(main())
