import aiohttp
from fake_useragent import UserAgent
from datetime import datetime
from colorama import *
import asyncio
import json
import base64
import hashlib
import string
import random
import os
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Bless:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": UserAgent().random
        }
        self.BASE_API = "https://gateway-run.bls.dev/api/v1"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.auth_tokens = {}
        self.ip_address = {}
        self.signatures = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.CYAN + Style.BRIGHT}Auto Ping Bless - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Real API Version - No Masking
            """
        )

    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text") as response:
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(f"Loaded {len(self.proxies)} proxies")
        
        except Exception as e:
            self.log(f"Failed To Load Proxies: {e}")
            self.proxies = []

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.proxies[self.proxy_index]
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.proxies[self.proxy_index]
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def decode_auth_token(self, token: str):
        try:
            header, payload, signature = token.split(".")
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
            parsed_payload = json.loads(decoded_payload)
            address = parsed_payload["publicAddress"]
            return address
        except Exception as e:
            return None
        
    def generate_hardware_info(self):
        cpu_models = ["AMD Ryzen 9 5900HS", "Intel Core i7-10700K", "AMD Ryzen 5 3600"]
        all_features = ["mmx", "sse", "sse2", "sse3", "ssse3", "sse4_1", "sse4_2", "avx", "avx2", "fma3", "aes", "pclmulqdq"]
        cpu_features = random.sample(all_features, k=random.randint(4, len(all_features)))
        
        return {
            "cpuArchitecture": "x86_64",
            "cpuModel": random.choice(cpu_models),
            "cpuFeatures": cpu_features,
            "numOfProcessors": len(cpu_features) * 2,
            "totalMemory": random.randint(8 * 1024**3, 64 * 1024**3)
        }
    
    def generate_hardware_id(self):
        return ''.join(random.choices(string.hexdigits.lower(), k=64))
    
    def generate_payload(self, pubkey: str, hardware_id: str):
        return {
            "ipAddress": self.ip_address[pubkey],
            "hardwareId": hardware_id,
            "hardwareInfo": self.generate_hardware_info(),
            "extensionVersion": "0.1.8"
        }
    
    def generate_signature(self):
        random_data = os.urandom(32)
        return hashlib.sha512(random_data).hexdigest()

    def print_status(self, account, pubkey, proxy, message, color=Fore.GREEN):
        print("\n" + "-"*40)
        print(f"Account: {account}")
        print(f"Pub Key: {pubkey}")
        print(f"Proxy: {proxy if proxy else 'No Proxy'}")
        print(f"Status: {color + Style.BRIGHT}{message}{Style.RESET_ALL}")
        print("-"*40)
        print("\nPlease support us:")
        print("Subscribe: https://youtube.com/forestarmy")
        print("Join Telegram: https://t.me/forestarmy")
        print("-"*40 + "\n")
        
    async def check_connection(self, address: str, pubkey: str, proxy=None):
        url = "https://ip-check.bless.network/"
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.ip_address[pubkey] = data["ip"]
                        self.signatures[pubkey] = self.generate_signature()
                        self.print_status(address, pubkey, proxy, "Connection successful")
                        return True
                    self.print_status(address, pubkey, proxy, f"Connection failed: {response.status}", Fore.RED)
        except Exception as e:
            self.print_status(address, pubkey, proxy, f"Connection error: {str(e)}", Fore.RED)
        return False
        
    async def node_uptime(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}"
        headers = {**self.headers, "Authorization": f"Bearer {self.auth_tokens[address]}"}
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 200:
                        return await response.json()
                    self.print_status(address, pubkey, proxy, f"Uptime check failed: {response.status}", Fore.RED)
        except Exception as e:
            self.print_status(address, pubkey, proxy, f"Uptime check error: {str(e)}", Fore.RED)
        return None
    
    async def register_node(self, address: str, pubkey: str, hardware_id: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}"
        data = self.generate_payload(pubkey, hardware_id)
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Type": "application/json",
            "X-Extension-Signature": self.signatures[pubkey],
            "X-Extension-Version": "0.1.8"
        }
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=data, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 429:
                        self.signatures[pubkey] = self.generate_signature()
                        return None
                    if response.status == 200:
                        return await response.json()
                    self.print_status(address, pubkey, proxy, f"Registration failed: {response.status}", Fore.RED)
        except Exception as e:
            self.print_status(address, pubkey, proxy, f"Registration error: {str(e)}", Fore.RED)
        return None
    
    async def start_session(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}/start-session"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Type": "application/json",
            "X-Extension-Signature": self.signatures[pubkey],
            "X-Extension-Version": "0.1.8"
        }
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json={}, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 429:
                        self.signatures[pubkey] = self.generate_signature()
                        return None
                    if response.status == 200:
                        return await response.json()
                    self.print_status(address, pubkey, proxy, f"Session start failed: {response.status}", Fore.RED)
        except Exception as e:
            self.print_status(address, pubkey, proxy, f"Session start error: {str(e)}", Fore.RED)
        return None
    
    async def send_ping(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}/ping"
        data = {"isB7SConnected": True}
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Type": "application/json",
            "X-Extension-Signature": self.signatures[pubkey],
            "X-Extension-Version": "0.1.8"
        }
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=data, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 429:
                        self.signatures[pubkey] = self.generate_signature()
                        return None
                    if response.status == 200:
                        return await response.json()
                    self.print_status(address, pubkey, proxy, f"Ping failed: {response.status}", Fore.RED)
        except Exception as e:
            self.print_status(address, pubkey, proxy, f"Ping error: {str(e)}", Fore.RED)
        return None
        
    async def process_account(self, account_data):
        auth_token = account_data["B7S_AUTH_TOKEN"]
        nodes = account_data["Nodes"]
        address = self.decode_auth_token(auth_token)
        
        if not auth_token or not nodes or not address:
            self.log(f"Invalid account data")
            return

        self.auth_tokens[address] = auth_token
        
        for node in nodes:
            pubkey = node.get("PubKey")
            hardware_id = node.get("HardwareId")
            
            if not pubkey or not hardware_id:
                continue
                
            proxy = self.get_next_proxy_for_account(pubkey)
            
            # Check connection
            if not await self.check_connection(address, pubkey, proxy):
                continue
                
            # Register node
            if not await self.register_node(address, pubkey, hardware_id, proxy):
                continue
                
            # Start session
            if not await self.start_session(address, pubkey, proxy):
                continue
                
            # Main ping loop
            while True:
                uptime = await self.node_uptime(address, pubkey, proxy)
                if uptime:
                    print(f"Uptime Today: {uptime.get('todayReward', 0)} mins")
                    print(f"Total Uptime: {uptime.get('totalReward', 0)} mins")
                
                await self.send_ping(address, pubkey, proxy)
                print("Waiting 10 minutes for next ping...")
                await asyncio.sleep(600)  # 10 minutes

    async def main(self):
        self.clear_terminal()
        self.welcome()
        
        accounts = self.load_accounts()
        if not accounts:
            self.log("No valid accounts found")
            return
            
        print("1. Use proxies from proxyscrape")
        print("2. Use local proxies")
        print("3. No proxies")
        choice = input("Select option (1-3): ")
        
        if choice in ["1", "2"]:
            await self.load_proxies(int(choice))
            
        rotate = input("Rotate invalid proxies? (y/n): ").lower() == "y"
        
        tasks = [self.process_account(account) for account in accounts]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        bot = Bless()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        print(f"Error: {e}")
