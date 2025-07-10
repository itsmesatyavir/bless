A lightweight Python script that **auto-pings the Bless Network** and helps you **earn reward points** using your token.

---

## 🎯 Features

- 🔁 Automatically pings the Bless Network
- 📥 Loads tokens from `token.txt`
- 🧠 Generates `accounts.json` automatically
- ▶️ Runs `main.py` to start earning points

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/itsmesatyavir/bless.git
cd bless
```

### 2. Install dependencies (if needed)

Currently, the script uses only built-in Python modules.  
If any external libraries are added later, install them with:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

### 1. Add your token(s)

Create a file named `token.txt` in the root folder and paste your token(s) inside.  
Add **one token per line** if using multiple accounts.

**Example `token.txt`:**

```
eyJhbGciOiJIUzI1NiIsInR...
eyJ0eXAiOiJKV1QiLCJh...
```

### 2. Run the script

```bash
python run.py
```

This will:
- Read your tokens from `token.txt`
- Auto-create `accounts.json`
- Start the auto-ping process via `main.py`

---

## 📁 Project Structure

```
bless/
├── LICENSE
├── README.md
├── token.txt            # ← Add your token(s) here
├── accounts.json        # ← Auto-generated
├── main.py              # ← Contains Bless Network ping logic
├── run.py               # ← Starts the automation
```

---

## 🧠 Notes

- Works with **Python 3.8+**
- Keep your `token.txt` safe and **do not share it**
- You can run this script on PC, VPS, or Termux

---

## 💬 Community

For help, updates, and discussions —  
Join us on Telegram: [@forestarmy](https://t.me/forestarmy)
