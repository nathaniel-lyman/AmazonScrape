# AmazonScrape

AmazonScrape is a tool that identifies which U.S. metro areas have Amazon Fresh Delivery service available. It uses a headless Playwright-based scraper to check the availability of Amazon Fresh delivery by ZIP code.

## Features

- Determines Amazon Fresh Delivery availability across metro areas.
- Automates browser actions using Playwright in headless mode.
- Persists Amazon login credentials for seamless subsequent scraping sessions.

## Requirements

- Node.js (ensure you have the latest LTS version)
- [Playwright](https://playwright.dev/)
- An Amazon account with Amazon Fresh access

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/nathaniel-lyman/amazon-scrape.git
    cd amazon-scrape
    ```

2. Install dependencies:

    ```sh
    npm install
    # or
    yarn install
    ```

3. Install Playwright browsers (if not automatically installed):

    ```sh
    npx playwright install
    ```

## Usage

### 1. Initial Login

The script requires you to log in to your Amazon account once. This ensures that the scraper can access delivery availability pages as an authenticated user.

```sh
node login.js
```

Follow the prompts to log in via the automated browser window. Your session will be saved for future runs.

### 2. Run the Scraper

After logging in, you can run the scraper to check Amazon Fresh delivery by ZIP code:

```sh
node scrape.js --zipcodes path/to/zipcodes.txt
```

- Replace `path/to/zipcodes.txt` with your file containing a list of ZIP codes (one per line).

### Example

```sh
node scrape.js --zipcodes metro_zips.txt --output results.json
```

- This will check each ZIP code in `metro_zips.txt` and write the results to `results.json`.

## Configuration

- **ZIP code file:** Plain text file with one ZIP code per line.
- **Output:** JSON or CSV formats supported (customize based on your script).
- **Session storage:** Login session is stored locally (specify path if needed).

## Notes

- **Legal:** Scraping Amazon may violate their terms of service. Use at your own risk and for educational purposes only.
- **Stability:** Amazon's site structure may change, requiring script updates.
- **Performance:** Headless scraping is more efficient, but some features may require a visible browser.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

---

*This project is not affiliated with or endorsed by Amazon.com, Inc.*
