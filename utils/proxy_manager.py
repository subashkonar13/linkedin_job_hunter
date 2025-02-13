import random
from typing import List, Optional
import requests

class ProxyManager:
    def __init__(self, proxy_list_url: str):
        self.proxies = []
        self.last_update = None
        self.proxy_list_url = proxy_list_url
        
    async def get_proxy(self) -> Optional[dict]:
        if self._should_update_proxies():
            await self._update_proxy_list()
        return random.choice(self.proxies) if self.proxies else None
        
    async def _update_proxy_list(self):
        """Update proxy list from provider"""
        try:
            response = requests.get(self.proxy_list_url)
            self.proxies = response.json()
        except Exception as e:
            print(f"Failed to update proxy list: {e}")
