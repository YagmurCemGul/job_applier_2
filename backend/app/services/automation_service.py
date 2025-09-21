import asyncio
import random
from playwright.async_api import async_playwright, Page, Browser

class BasePlatformAdapter:
    """
    Abstract base class for a platform-specific automation adapter.
    It defines the common interface for all job platforms.
    """
    def __init__(self, browser: Browser):
        if not browser:
            raise ValueError("A Playwright Browser instance is required.")
        self.browser = browser
        self.page = None

    async def initialize(self):
        """Initializes a new browser page for the adapter to use."""
        self.page = await self.browser.new_page()
        # Emulate a common user agent to avoid basic detection
        await self.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        print(f"[{self.__class__.__name__}] New page initialized.")

    async def login(self, credentials: dict):
        """Logs into the platform."""
        raise NotImplementedError("The 'login' method must be implemented by a subclass.")

    async def search_jobs(self, search_criteria: dict) -> list:
        """Searches for jobs based on given criteria and returns a list of job URLs."""
        raise NotImplementedError("The 'search_jobs' method must be implemented by a subclass.")

    async def get_job_details(self, job_url: str) -> dict:
        """Extracts detailed information from a job posting page."""
        raise NotImplementedError("The 'get_job_details' method must be implemented by a subclass.")

    async def apply_to_job(self, job_url: str, application_data: dict):
        """Navigates to the application page and fills out the form."""
        raise NotImplementedError("The 'apply_to_job' method must be implemented by a subclass.")

    async def _human_like_delay(self, min_seconds=1, max_seconds=3):
        """Waits for a random duration to mimic human behavior."""
        delay = random.uniform(min_seconds, max_seconds)
        print(f"Waiting for {delay:.2f} seconds...")
        await asyncio.sleep(delay)

    async def close(self):
        """Closes the browser page."""
        if self.page:
            await self.page.close()
            print(f"[{self.__class__.__name__}] Page closed.")


class LinkedInAdapter(BasePlatformAdapter):
    """
    Automation adapter for LinkedIn.
    (This is a placeholder implementation)
    """
    BASE_URL = "https://www.linkedin.com"

    async def login(self, credentials: dict):
        print(f"[{self.__class__.__name__}] Navigating to login page...")
        await self.page.goto(f"{self.BASE_URL}/login")
        await self._human_like_delay()

        print(f"[{self.__class__.__name__}] Filling in credentials (username: {credentials.get('email')})...")
        await self.page.fill("#username", credentials.get("email", ""))
        await self.page.fill("#password", credentials.get("password", ""))
        await self.page.click("button[type='submit']")

        # Wait for navigation to complete, e.g., by checking for the feed page
        await self.page.wait_for_selector("#feed-tab-icon", timeout=60000)
        print(f"[{self.__class__.__name__}] Login successful.")

    async def search_jobs(self, search_criteria: dict) -> list:
        print(f"[{self.__class__.__name__}] Searching for jobs with criteria: {search_criteria}")
        # Placeholder for actual search logic
        # e.g., await self.page.goto(f"{self.BASE_URL}/jobs/search/?keywords={search_criteria.get('title')}")
        await self._human_like_delay()
        print(f"[{self.__class__.__name__}] Found 5 placeholder job URLs.")
        return ["https://linkedin.com/jobs/view/1", "https://linkedin.com/jobs/view/2"]

    async def get_job_details(self, job_url: str) -> dict:
        print(f"[{self.__class__.__name__}] Navigating to job URL: {job_url}")
        await self.page.goto(job_url)
        await self._human_like_delay()
        # Placeholder for data extraction
        job_title = await self.page.locator('h1').first.text_content()
        job_description = await self.page.locator('.jobs-description__content').first.text_content()
        print(f"[{self.__class__.__name__}] Extracted job title: {job_title}")
        return {"title": job_title, "description": job_description.strip()}


class AutomationController:
    """
    Selects the correct platform adapter and manages the automation process.
    """
    def __init__(self, browser: Browser):
        self._browser = browser
        self._adapters = {
            "linkedin": LinkedInAdapter(browser),
            # "indeed": IndeedAdapter(browser), # Example for future extension
        }

    def get_adapter(self, platform_name: str) -> BasePlatformAdapter:
        adapter = self._adapters.get(platform_name.lower())
        if not adapter:
            raise ValueError(f"No adapter found for platform: {platform_name}")
        return adapter

# Example usage (for testing purposes)
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        controller = AutomationController(browser)

        linkedin_adapter = controller.get_adapter("linkedin")
        await linkedin_adapter.initialize()

        # This would fail without real credentials, so it's commented out.
        # await linkedin_adapter.login({"email": "your-email", "password": "your-password"})

        job_urls = await linkedin_adapter.search_jobs({"title": "Software Engineer"})
        if job_urls:
            details = await linkedin_adapter.get_job_details(job_urls[0])
            print("Extracted Details:", details)

        await linkedin_adapter.close()
        await browser.close()

if __name__ == "__main__":
    # To run this file for testing: python -m app.services.automation_service
    asyncio.run(main())
