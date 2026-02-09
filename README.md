# 🚀 LLaMA 3.1 GPU Chatbot (Docker + Streamlit + FastAPI)

A **production-style chatbot** powered by **LLaMA 3.1**, running fully on **GPU**, with a clean separation of concerns.

### Tech Stack
- 🧠 **Ollama** (LLaMA 3.1 on GPU)
- ⚙️ **FastAPI** (Backend API)
- 🎨 **Streamlit** (Frontend UI)
- 🐳 **Docker & Docker Compose**

---

## 🏗️ Architecture

Browser  
↓  
Streamlit Frontend  
↓ (HTTP)  
FastAPI Backend  
↓  
Ollama (LLaMA 3.1 on GPU)

---

## 📁 Project Structure

```
llama-chatbot/
│
├── frontend/
│   ├── app.py
│   └── Dockerfile
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## ✅ Prerequisites

### Hardware
- NVIDIA GPU (RTX / GTX)
- 8 GB VRAM minimum (RTX 3060 / 4060 recommended)

### Software
- Windows 10/11
- Docker Desktop
- WSL 2 enabled
- NVIDIA GPU drivers

Verify GPU:
```powershell
nvidia-smi
```

Verify Docker:
```powershell
docker --version
```

---

## 🐧 Enable WSL 2 (One-Time Setup)

Open **PowerShell as Administrator**:

```powershell
wsl --install
```

Restart your PC.

Verify:
```powershell
wsl --status
```

---

## ▶️ How to Start the Chatbot

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/llama-chatbot.git
cd llama-chatbot
```

---

### 2️⃣ Start All Services (Docker)

```powershell
docker compose up --build
```

⏳ First run may take several minutes.

---

### 3️⃣ Download LLaMA 3.1 Model (One Time)

Open a **new terminal**:

```powershell
docker exec -it llama-chatbot-ollama-1 ollama pull llama3.1
```

---

### 4️⃣ Open the Chatbot UI

Open your browser:

👉 http://localhost:8501

You can now chat with LLaMA 3.1 🎉

---

## 🧪 Verify GPU Usage

### System-wide GPU usage
```powershell
nvidia-smi -l 1
```

### GPU usage inside Ollama container
```powershell
docker exec -it llama-chatbot-ollama-1 nvidia-smi
```

### Ollama logs (definitive proof)
```powershell
docker logs llama-chatbot-ollama-1
```

Look for lines like:
```
using CUDA
offloaded 33/33 layers to GPU
```

---

## ⚡ Performance Notes

| Mode | Typical Response Time |
|----|------------------------|
| CPU | 20–60 seconds |
| GPU | 0.5–3 seconds |

The **first request** is slower due to model loading.

---

## 🛠️ Stop the Server

```powershell
docker compose down
```

---

## 🔧 GPU Configuration (Already Enabled)

```yaml
environment:
  - OLLAMA_NUM_GPU=1
  - OLLAMA_FLASH_ATTENTION=1
```

---

## 🚀 Future Improvements

- Token-by-token streaming
- Authentication (JWT)
- Persistent chat history (DB)
- Multi-user support
- Cloud GPU deployment

---

## 📜 License

MIT License

---

## ⭐ Support

If this project helped you, consider giving it a ⭐ on GitHub!
