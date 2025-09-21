import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
from ..core.security import get_credential
from ..core.prompt_library import get_cv_optimization_prompt, get_cover_letter_prompt

# --- Configuration Loader ---

def _load_selectors():
    """Loads the CSS selectors from the JSON file."""
    selectors_path = Path(__file__).parent.parent / "core" / "selectors.json"
    with open(selectors_path, 'r') as f:
        return json.load(f)

SELECTORS = _load_selectors()

# --- Base Class for AI Web Interaction ---

class BaseAIInteractor:
    """
    Abstract base class for an AI web UI automation interactor.
    Manages a Playwright page and defines the interaction workflow.
    """
    def __init__(self, browser: Browser, service_name: str):
        if not browser:
            raise ValueError("A Playwright Browser instance is required.")
        self.browser = browser
        self.service_name = service_name
        self.selectors = SELECTORS.get(service_name)
        if not self.selectors:
            raise ValueError(f"Selectors for service '{service_name}' not found in selectors.json")
        self.page = None

    async def initialize(self):
        """Initializes a new browser page for interaction."""
        self.page = await self.browser.new_page()
        print(f"[{self.service_name}] New page initialized.")

    async def login(self, username: str, password: str):
        """Placeholder for logging into the service."""
        print(f"[{self.service_name}] Navigating to login page: {self.selectors['login_url']}")
        await self.page.goto(self.selectors['login_url'])

        print(f"[{self.service_name}] Filling username...")
        await self.page.fill(self.selectors['username_input'], username)
        # Some sites require a 'continue' click after username
        if self.selectors.get('username_continue_button'):
            await self.page.click(self.selectors['username_continue_button'])

        print(f"[{self.service_name}] Filling password...")
        await self.page.fill(self.selectors['password_input'], password)

        print(f"[{self.service_name}] Clicking login button...")
        await self.page.click(self.selectors['login_button'])
        await self.page.wait_for_load_state('networkidle')
        print(f"[{self.service_name}] Login process completed.")

    async def send_prompt(self, prompt: str) -> str:
        """Sends a prompt to the chat interface and gets the response."""
        print(f"[{self.service_name}] Typing prompt into: {self.selectors['chat_input_box']}")
        await self.page.fill(self.selectors['chat_input_box'], prompt)

        print(f"[{self.service_name}] Clicking send button...")
        await self.page.click(self.selectors['send_button'])

        # Wait for the response to be complete.
        # A robust way is to wait for the "stop generating" button to disappear.
        stop_button_selector = self.selectors['stop_generating_button']
        print(f"[{self.service_name}] Waiting for response to complete (waiting for '{stop_button_selector}' to be hidden)...")
        await self.page.wait_for_selector(stop_button_selector, state='hidden', timeout=120000)

        print(f"[{self.service_name}] Scraping response from: {self.selectors['last_response_element']}")
        response_text = await self.page.locator(self.selectors['last_response_element']).last.inner_text()
        return response_text.strip()

    async def close(self):
        """Closes the page."""
        if self.page:
            await self.page.close()

# --- Concrete Implementations ---

class ChatGPTInteractor(BaseAIInteractor):
    def __init__(self, browser: Browser):
        super().__init__(browser, "openai")

class GeminiInteractor(BaseAIInteractor):
    def __init__(self, browser: Browser):
        super().__init__(browser, "google")

class ClaudeInteractor(BaseAIInteractor):
    def __init__(self, browser: Browser):
        super().__init__(browser, "anthropic")


# --- Main Engine Controller ---

class AIEngine:
    """
    Manages AI interaction by selecting the appropriate web interactor.
    """
    def __init__(self, browser: Browser):
        self._browser = browser
        self._interactors = {
            "openai": ChatGPTInteractor(browser),
            "google": GeminiInteractor(browser),
            "anthropic": ClaudeInteractor(browser),
        }

    def get_interactor(self, service_name: str) -> BaseAIInteractor:
        """Gets the interactor instance for the specified service."""
        interactor = self._interactors.get(service_name.lower())
        if not interactor:
            raise ValueError(f"No interactor found for service: {service_name}")
        return interactor

# Example usage
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        engine = AIEngine(browser)

        # 1. Get the right interactor
        service = "openai"
        interactor = engine.get_interactor(service)
        await interactor.initialize()

        # 2. Get credentials securely
        # NOTE: In the real app, the username would be stored in the local DB.
        # For this test, we'll hardcode it.
        username_to_test = "test@example.com"
        password = get_credential(service, username_to_test)

        if password:
            # This part would run in the real app if credentials are found
            print(f"Found password for {username_to_test}, proceeding with login.")
            # await interactor.login(username_to_test, password)
            # response = await interactor.send_prompt("Hello, world!")
            # print("AI Response:", response)
        else:
            print(f"Could not find password for {username_to_test} in keychain. Skipping interaction.")

        await interactor.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
