import pandas as pd
from playwright.sync_api import sync_playwright
import time
import logging

# 🔢 Major ZIPs across the U.S.
ZIPS_TO_TEST = [
    {"zip": "10001", "city": "New York", "state": "NY", "population": 21102},
    {"zip": "90001", "city": "Los Angeles", "state": "CA", "population": 57110},
    {"zip": "60601", "city": "Chicago", "state": "IL", "population": 10871},
    {"zip": "77001", "city": "Houston", "state": "TX", "population": 65000},
    {"zip": "85001", "city": "Phoenix", "state": "AZ", "population": 32000},
    {"zip": "19104", "city": "Philadelphia", "state": "PA", "population": 52772},
    {"zip": "75201", "city": "Dallas", "state": "TX", "population": 26584},
    {"zip": "20001", "city": "Washington", "state": "DC", "population": 38635},
    {"zip": "30303", "city": "Atlanta", "state": "GA", "population": 21000},
    {"zip": "98101", "city": "Seattle", "state": "WA", "population": 12295}
]

# 🪵 Logging setup
logging.basicConfig(
    filename="fresh_zip_dom_toaster.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

results = []

def check_zip(playwright, zip_code, retry=0):
    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="amazon_state.json")
        page = context.new_page()

        fresh_url = "https://www.amazon.com/alm/storefront?almBrandId=QW1hem9uIEZyZXNo"
        page.goto(fresh_url)
        page.wait_for_timeout(3000)

        # Step 2: Open ZIP modal and enter ZIP slowly
        page.click("#nav-global-location-popover-link", force=True)
        page.wait_for_selector("#GLUXZipUpdateInput", timeout=10000)
        page.click("#GLUXZipUpdateInput")

        print(f"⌨️ Typing ZIP: {zip_code}")
        for char in zip_code:
            page.keyboard.insert_text(char)
            page.wait_for_timeout(100)

        # Click Apply
        apply_btn = page.query_selector("#GLUXZipUpdate")
        if apply_btn and apply_btn.is_visible():
            print("✅ Clicking Apply...")
            apply_btn.click(force=True)
        else:
            print("❌ Apply button not found or not visible")
        page.wait_for_timeout(3000)

        # Click Done
        done_btn = page.query_selector('button[name="glowDoneButton"]')
        if done_btn and done_btn.is_visible():
            print("✅ Clicking Done...")
            done_btn.click(force=True)
            page.wait_for_timeout(2000)
        else:
            print("❌ Done button not found or not visible")

        # Step 3: Simulate real user interaction
        print("🧠 Simulating human-like behavior...")
        try:
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(500)

            hover_target = page.query_selector("#nav-cart")
            if hover_target:
                page.hover("#nav-cart")
                page.wait_for_timeout(500)

            tile = page.query_selector("div[data-testid='almShelfContainer'] a")
            if tile:
                tile.click()
                page.wait_for_timeout(2000)
                page.go_back()
                page.wait_for_timeout(2000)
        except Exception as e:
            print(f"⚠️ Interaction error: {e}")

        # Step 4: Reload to lock ZIP and catch toaster
        page.goto(fresh_url)
        page.wait_for_timeout(5000)

        # Step 5: DOM toaster check
        toaster = page.query_selector('div[data-toaster-type="ALM_ADDRESS_INELIGIBLE"]')
        eligible = toaster is None

        logging.info(f"ZIP {zip_code}: {'✅ Eligible' if eligible else '❌ Not Eligible'}")
        browser.close()
        return eligible

    except Exception as e:
        logging.error(f"ZIP {zip_code} attempt {retry+1} failed: {e}")
        try:
            browser.close()
        except:
            pass
        if retry < 2:
            time.sleep(2 + retry)
            return check_zip(playwright, zip_code, retry + 1)
        return False

# ✅ Run the check
with sync_playwright() as p:
    for row in ZIPS_TO_TEST:
        zip_code = str(row["zip"]).zfill(5)
        print(f"🔍 Checking ZIP {zip_code} ({row['city']}, {row['state']})...")
        is_eligible = check_zip(p, zip_code)
        results.append({
            "zip": zip_code,
            "city": row["city"],
            "state": row["state"],
            "population": row["population"],
            "eligible": is_eligible
        })

# 💾 Save results
df = pd.DataFrame(results)
df.to_csv("fresh_eligibility_toaster_results.csv", index=False)

print("\n✅ Done! Results saved to fresh_eligibility_toaster_results.csv")
print("🪵 Log saved to fresh_zip_dom_toaster.log")