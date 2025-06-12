from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("🚀 Launching Chromium browser...")
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Go directly to Amazon login
    page.goto("https://www.amazon.com/ap/signin")

    print("\n🔐 Please log into Amazon in the browser window.")
    print("🕒 After you've logged in and see the Amazon homepage, come back here.")
    input("👉 Press ENTER in the terminal to save session and close browser...")

    # Save cookies after manual login
    context.storage_state(path="amazon_state.json")
    print("✅ Session saved to amazon_state.json")

    browser.close()
