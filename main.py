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
        {Fore.CYAN + Style.BRIGHT}Auto Ping Bless Script
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}JOIN:- t.me/forestarmy {Fore.YELLOW + Style.BRIGHT} Thank You Vonssy
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
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

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
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
        
    def mask_account(self, account):
        return account[:6] + '*' * 6 + account[-6:]

    def print_message(self, account, pub_key, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Pub Key: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{self.mask_account(pub_key)}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Proxy:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Status: {Style.RESET_ALL}"
            f"{color + Style.BRIGHT}{message}{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} ]{Style.RESET_ALL}"
        )
        
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = "With Free Proxyscrape" if choose == 1 else "With Private" if choose == 2 else "Without"
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()
                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def check_connection(self, address: str, pubkey: str, proxy=None):
        url = "https://ip-check.bless.network/"
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.ip_address[pubkey] = data["ip"]
                        self.signatures[pubkey] = self.generate_signature()
                        self.print_message(address, pubkey, proxy, Fore.GREEN, "Connection 200 OK")
                        return True
                    self.print_message(address, pubkey, proxy, Fore.RED, f"Connection Not 200 OK: {response.status}")
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"Connection Error: {str(e)}")
        return False
        
    async def node_uptime(self, address: str, pubkey: str, proxy=None):
        url = f"{self.BASE_API}/nodes/{pubkey}"
        headers = {**self.headers, "Authorization": f"Bearer {self.auth_tokens[address]}"}
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, proxy=proxy, timeout=aiohttp.ClientTimeout(total=60), ssl=False) as response:
                    if response.status == 200:
                        return await response.json()
                    self.print_message(address, pubkey, proxy, Fore.RED, f"GET Node Uptime Failed: {response.status}")
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"GET Node Uptime Error: {str(e)}")
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
                    self.print_message(address, pubkey, proxy, Fore.RED, f"Registering Node Failed: {response.status}")
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"Registering Node Error: {str(e)}")
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
                    self.print_message(address, pubkey, proxy, Fore.RED, f"Starting Session Failed: {response.status}")
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"Starting Session Error: {str(e)}")
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
                    self.print_message(address, pubkey, proxy, Fore.RED, f"PING Failed: {response.status}")
        except Exception as e:
            self.print_message(address, pubkey, proxy, Fore.RED, f"PING Error: {str(e)}")
        return None
        
    async def process_check_connection(self, address: str, pubkey: str, use_proxy: bool, rotate_proxy: bool):
        proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

        if rotate_proxy:
            while True:
                if await self.check_connection(address, pubkey, proxy):
                    return True
                proxy = self.rotate_proxy_for_account(pubkey) if use_proxy else None
                await asyncio.sleep(5)
        else:
            while True:
                if await self.check_connection(address, pubkey, proxy):
                    return True
                await asyncio.sleep(5)
        
    async def process_register_node(self, address: str, pubkey: str, hardware_id: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

        while True:
            if await self.register_node(address, pubkey, hardware_id, proxy):
                self.print_message(address, pubkey, proxy, Fore.GREEN, "Registering Node Success")
                return True
            await asyncio.sleep(5)
        
    async def process_start_session(self, address: str, pubkey: str, hardware_id: str, use_proxy: bool):
        if await self.process_register_node(address, pubkey, hardware_id, use_proxy):
            proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

            while True:
                result = await self.start_session(address, pubkey, proxy)
                if isinstance(result, dict) and result.get("status") == "ok":
                    self.print_message(address, pubkey, proxy, Fore.GREEN, "Starting Session Success")
                    return True
                await asyncio.sleep(5)
            
    async def process_send_ping(self, address: str, pubkey: str, hardware_id: str, use_proxy: bool):
        if await self.process_start_session(address, pubkey, hardware_id, use_proxy):
            while True:
                proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}Try to Sent Ping...{Style.RESET_ALL}                                         ",
                    end="\r",
                    flush=True
                )

                result = await self.send_ping(address, pubkey, proxy)
                if isinstance(result, dict) and result.get("status") == "ok":
                    self.print_message(address, pubkey, proxy, Fore.GREEN, "PING Success")

                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}Wait For 10 Minutes For Next Ping...{Style.RESET_ALL}",
                    end="\r"
                )
                
                await asyncio.sleep(10 * 60)
        
    async def process_get_node_uptime(self, address: str, pubkey: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(pubkey) if use_proxy else None

            node = await self.node_uptime(address, pubkey, proxy)
            if node:
                today_reward = node.get("todayReward", 0)
                total_reward = node.get("totalReward", 0)

                self.print_message(address, pubkey, proxy, Fore.GREEN, "Uptime Updated"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Uptime Today:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {today_reward} Minutes {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{total_reward} Minutes{Style.RESET_ALL}"
                )

            await asyncio.sleep(30 * 60)

    async def process_accounts(self, address: str, nodes: list, use_proxy: bool, rotate_proxy: bool):
        tasks = []

        async def process_node_session(node):
            pubkey = node.get("PubKey")
            hardware_id = node.get("HardwareId")

            if pubkey and hardware_id:
                if await self.process_check_connection(address, pubkey, use_proxy, rotate_proxy):
                    tasks.append(asyncio.create_task(self.process_get_node_uptime(address, pubkey, use_proxy)))
                    tasks.append(asyncio.create_task(self.process_send_ping(address, pubkey, hardware_id, use_proxy)))

        await asyncio.gather(*[process_node_session(node) for node in nodes if node])
        await asyncio.gather(*tasks)
        
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice, rotate_proxy = self.print_question()
            use_proxy = use_proxy_choice in [1, 2]

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*75)

            tasks = []
            for idx, account in enumerate(accounts, start=1):
                if account:
                    auth_token = account["B7S_AUTH_TOKEN"]
                    nodes = account["Nodes"]

                    if not auth_token or not nodes:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Account Data {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    address = self.decode_auth_token(auth_token)
                    if not address:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid B7S Auth Token {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    self.auth_tokens[address] = auth_token
                    tasks.append(asyncio.create_task(self.process_accounts(address, nodes, use_proxy, rotate_proxy)))

            await asyncio.gather(*tasks)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Bless()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Bless - BOT{Style.RESET_ALL}                                       "                              
        )
