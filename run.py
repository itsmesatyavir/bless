import requests
import json
import os
import subprocess

API_URL = "https://gateway-run-indexer.bls.dev/api/v1/nodes"
TOKENS_FILE = "token.txt"
OUTPUT_FILE = "accounts.json"
MAIN_SCRIPT = "main.py"

def read_tokens(filename):
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_nodes(auth_token):
    # Ensure token starts with "Bearer "
    if not auth_token.lower().startswith("bearer "):
        auth_token = "Bearer " + auth_token

    headers = {
        "Authorization": auth_token,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed for token: {auth_token[:50]}... — {e}")
        return []

def run_main_script():
    if not os.path.exists(MAIN_SCRIPT):
        print(f"⚠️ main.py not found. Skipping execution.")
        return
    print(f"\n🚀 Running {MAIN_SCRIPT}...\n")
    subprocess.run(["python", MAIN_SCRIPT], check=False)

def main():
    tokens = read_tokens(TOKENS_FILE)
    if not tokens:
        return

    accounts = []

    for token in tokens:
        nodes = fetch_nodes(token)
        if not isinstance(nodes, list):
            continue

        node_list = []
        for node in nodes:
            pubkey = node.get("pubKey")
            node_id = node.get("_id")
            if pubkey and node_id:
                node_list.append({
                    "PubKey": pubkey,
                    "HardwareId": node_id
                })

        accounts.append({
            "B7S_AUTH_TOKEN": token,
            "Nodes": node_list
        })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

    print(f"✅ Saved {len(accounts)} accounts to {OUTPUT_FILE}")

    # Run main.py
    run_main_script()

if __name__ == "__main__":
    main()
