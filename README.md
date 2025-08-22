# 🚗✨ Parkify — *Book Your Parking Spot with Ease*

Welcome to **Parkify**, your go-to solution to *escape the parking mayhem* and seamlessly **reserve your spot** ahead of time — because spending 20 minutes looking for parking is so 2010.

Minimal clicks. Maximum convenience.
**Park smart. Park easy. Parkify.**

---

## 💡 What is Parkify?

**Parkify** is a modern, user-friendly web application that lets you book a parking spot *before* you arrive. Whether you're heading downtown or attending a packed event, you're just a tap away from guaranteed peace of mind.

---

## 🚀 Quick Start — Run Parkify Locally

Before diving in, make sure you have **[UV](https://docs.astral.sh/uv/)** installed — it's a blazing-fast Python package manager that makes bootstrapping your project effortless.

### ✅ Step 1: Install UV

```bash
pip install uv
```

### 🔐 Step 2: Set Up Your Environment

Create your own `.env` file based on the sample provided:

```bash
FLASK_DEBUG = ...
FLASK_RUN_HOST = ...
FLASK_RUN_PORT = ...
CACHE_TYPE = ...


SECRET_KEY = ...


SQLALCHEMY_DATABASE_URI = ...
SQLALCHEMY_TRACK_MODIFICATIONS = ...


ADMIN_MAIL = ...
ADMIN_PASSWORD = ...
ADMIN_NAME = ...
ADMIN_PINCODE = ...
ADMIN_ADDRESS = ...

SECONDS = ...

SESSION_REFRESH_EACH_REQUEST = ...
SESSION_PERMANENT = ...


SECURITY_LOGIN_URL = ...
SECURITY_LOGOUT_URL = ...
SECURITY_REGISTERABLE = ...
SECURITY_SEND_REGISTER_EMAIL = ...
SECURITY_USERNAME_ENABLE = ...
```

Then, open `.env` and edit the values (such as `FLASK_SECRET_KEY`, `DB_URI`, etc.) according to your local setup.

### ⚡️ Step 3: Run the App

Launch the app with one simple command:

```bash
uv run flask run
```

This will:

* Automatically create a virtual environment
* Install all dependencies from `pyproject.toml`
* Start the **Flask** development server

### 🌐 Step 4: You're Live!

Your Parkify app will be available at:

```
http://localhost:5000/
```

*(Or whatever port Flask assigns — check your terminal output.)*

---

## 🛠 Tech Stack

* **Flask** – Python web framework
* **UV** – Fast dependency and environment manager
* **HTML, CSS, JS** – For a clean and responsive frontend

---

## 💖 Made with Love

Parkify is crafted with a passion for solving real-world problems — no stress, no chaos, just pure parking bliss.

---

## 👑 Park Like Royalty

No more circling blocks.
No more awkward valet interactions.
Just you, your ride, and a perfectly timed parking spot.

**Parkify** — *because parking should be predictable.*
