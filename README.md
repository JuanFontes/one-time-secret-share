# 🔐 one-time-secret-share - [![CI - One-Time Secret Share](https://github.com/JuanFontes/one-time-secret-share/actions/workflows/ci.yml/badge.svg)](https://github.com/JuanFontes/one-time-secret-share/actions/workflows/ci.yml)

A lightweight, one-time secret sharing app built with Flask — fully Dockerized and ready to deploy! Share sensitive messages securely, once and only once. 🔥

---

## ✨ Features

- 🔒 Secrets can only be viewed once
- 🧾 Friendly message if the secret has expired or was already viewed
- 🌐 Minimal UI using HTML + Bootstrap
- 🐳 Fully Dockerized with support for Docker Compose
- 🧪 Simple to test with `pytest`

---

## 🚀 How It Works

1. Submit a secret through the web form.
2. The app generates a unique, one-time access link.
3. The recipient views it **once** — then it's gone.
4. If reused or expired, the user sees an informative message.

---

## 🧰 Tech Stack

- Python 3.11
- Flask
- HTML + Bootstrap
- Docker & Docker Compose
- Pytest

---

## 🛠️ Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/JuanFontes/one-time-secret-share.git
cd one-time-secret-share
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Setup

This app uses a Fernet encryption key to securely store and retrieve secrets.

### 🔐 Generate a Fernet Key

You can generate a Fernet key using Python:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 📝 Create a `.env` file

Create a `.env` file in your project root and add the generated key:

```bash
SECRET_KEY=your_generated_key_here
```

Make sure to keep this key **secret** and never commit your `.env` file to version control!


### 4. Run the app

```bash
python app/main.py
```

---

## 🐳 Running with Docker

```bash
docker build -t one-time-secret-share .
docker run -p 5000:5000 one-time-secret-share
```

---

## 🐙 Run with Docker Compose

```bash
docker compose up --build
```

Then open: [http://localhost:5000](http://localhost:5000)

---

## ✅ Running Tests

```bash
pytest
```

---

## 📂 Project Structure

```
├── app/
│   ├── main.py          # Flask app
│   ├── templates/       # HTML templates
│   └── static/          # Optional CSS/JS
├── tests/               # Unit tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more information.

---

## 🤝 Contributing

Pull requests are welcome! Open an issue for feature requests or bugs.

