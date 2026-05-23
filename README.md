# 🚀 HackArena TechSpark

### 🚀 AI-Powered Compensation Data Validation

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/AI-Powered-black?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Cybersecurity-Threat%20Intelligence-red?style=for-the-badge"/>
</p>

<p align="center">
  <b>Real-Time Threat Detection • AI Security Analytics • Threat Intelligence Dashboard</b>
</p>

---

# 🌐 Live Demo

## 🔗 Frontend Dashboard

[https://bhavana998-hackarena-techspark-dashboardapp-3paiwk.streamlit.app/](https://bhavana998-hackarena-techspark-dashboardapp-3paiwk.streamlit.app/)

## ⚡ Backend API

[https://hackarena-techspark.onrender.com](https://hackarena-techspark.onrender.com)

---

# 🧠 About The Project

HackArena TechSpark is a production-ready AI cybersecurity intelligence platform developed to simulate modern Security Operations Center (SOC) workflows.

The system helps organizations detect, analyze, and monitor cyber threats using Machine Learning, real-time analytics, and intelligent alert management.

Unlike traditional monitoring tools, HackArena TechSpark focuses on:

* ⚡ AI-powered threat severity prediction
* 🛡️ Intelligent attack analysis
* 📊 Real-time analytics visualization
* 🚨 Security alert prioritization
* ☁️ Cloud-native deployment architecture

The platform demonstrates full-stack engineering capabilities by combining:

* FastAPI backend services
* Streamlit interactive dashboard
* Machine Learning prediction pipeline
* Cloud deployment on Render & Streamlit Cloud
* Real-time cybersecurity analytics

---

# ✨ Key Features

## 🛡️ AI Threat Detection

* Detect abnormal cybersecurity events
* Analyze attack patterns
* Predict threat severity using Machine Learning

---

## 📊 Interactive Dashboard

* Real-time analytics visualization
* Threat monitoring dashboard
* Security event insights
* Attack trend analysis

---

## ⚡ FastAPI Production Backend

* Scalable REST API architecture
* High-performance backend services
* Cloud deployment ready

---

## 🚨 Smart Alert System

* Automated security alerts
* Threat prioritization
* Incident categorization

---

## ☁️ Cloud-Native Deployment

* Backend deployed on Render
* Frontend deployed using Streamlit Cloud
* Publicly accessible architecture

---

# 🏗️ Enterprise Architecture

````text
┌───────────────────────────────────────────────┐
│            Streamlit Frontend UI             │
│      Real-Time Security Monitoring Dashboard │
└──────────────────────┬────────────────────────┘
                       │
                       │ REST API Requests
                       ▼
┌───────────────────────────────────────────────┐
│              FastAPI Backend API             │
│     Threat Detection & Alert Management      │
└──────────────────────┬────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────────┐      ┌───────────────────┐
│  ML Prediction    │      │ Security Analytics│
│ Severity Engine   │      │ & Threat Insights │
└───────────────────┘      └───────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│        Threat Intelligence & Alert System    │
└───────────────────────────────────────────────┘
```text
                     ┌──────────────────────┐
                     │  Streamlit Frontend  │
                     │ Security Dashboard   │
                     └──────────┬───────────┘
                                │
                                │ REST API Calls
                                ▼
                     ┌──────────────────────┐
                     │   FastAPI Backend    │
                     │ Threat Intelligence  │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │   ML Prediction      │
                     │ Severity Detection   │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Analytics & Alerts   │
                     └──────────────────────┘
````

---

# 🧰 Tech Stack

| Technology       | Purpose                    |
| ---------------- | -------------------------- |
| Python           | Core Development           |
| FastAPI          | Backend APIs               |
| Streamlit        | Frontend Dashboard         |
| Pandas           | Data Processing            |
| Plotly           | Interactive Visualizations |
| Machine Learning | Threat Prediction          |
| Render           | Backend Hosting            |
| Streamlit Cloud  | Frontend Deployment        |
| GitHub           | Version Control            |

---

# 📂 Project Structure

```bash
Hackarena-Techspark/
│
├── app.py                        # FastAPI backend entry point
├── requirements.txt              # Project dependencies
├── README.md
│
├── data/
│   └── cyber_threat_dataset.csv
│
├── models/
│   ├── trained_model.pkl
│   └── encoder.pkl
│
├── screenshots/
│   ├── dashboard-home.png
│   ├── threat-analytics.png
│   └── security-alerts.png
│
├── frontend/
│   └── dashboard.py              # Streamlit frontend dashboard
│
├── utils/
│   ├── preprocessing.py
│   ├── prediction.py
│   └── visualization.py
│
├── api/
│   ├── routes.py
│   └── schemas.py
│
└── notebooks/
    └── model_training.ipynb
```

---

# 📸 Application Screenshots

## 🖥️ Dashboard Overview

<img width="100%" src="screenshots/dashboard-home.png"/>

---

## 📊 Threat Analytics

<img width="100%" src="screenshots/threat-analytics.png"/>

---

## 🚨 Security Alerts

<img width="100%" src="screenshots/security-alerts.png"/>

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Bhavana998/Hackarena-Techspark.git
cd Hackarena-Techspark
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend Server

```bash
uvicorn app:app --reload
```

Backend URL:

```bash
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend Dashboard

```bash
streamlit run frontend/dashboard.py
```

Frontend URL:

```bash
http://localhost:8501
```

---

# 📡 API Endpoints

| Endpoint     | Method | Description               |
| ------------ | ------ | ------------------------- |
| `/`          | GET    | API Health Check          |
| `/predict`   | POST   | Predict Threat Severity   |
| `/alerts`    | GET    | Fetch Security Alerts     |
| `/analytics` | GET    | Retrieve Threat Analytics |

---

# 🔥 Production-Level Highlights

✅ Enterprise-Level Cybersecurity Dashboard
✅ AI-Powered Threat Severity Prediction
✅ Cloud-Native Deployment Architecture
✅ Real-Time Analytics & Monitoring
✅ Production FastAPI REST APIs
✅ Interactive Streamlit Visualization
✅ Scalable Backend Workflow
✅ End-to-End Full Stack AI System
✅ Recruiter & Hackathon Presentation Ready
✅ Publicly Deployed Live Project

---

# 🎯 Use Cases

* Security Operations Center (SOC)
* Threat Intelligence Systems
* Enterprise Security Monitoring
* AI-Based Incident Detection
* Cybersecurity Analytics Platforms
* Hackathon Demonstrations

---

# 🏆 Why This Project Stands Out

## 🚀 Real-World Cybersecurity Problem

Organizations receive thousands of alerts daily. This platform helps prioritize and analyze threats intelligently.

## 🧠 AI + Cybersecurity Integration

Combines Machine Learning with cybersecurity analytics to simulate modern SOC operations.

## ⚡ Full Stack Engineering

Demonstrates backend APIs, frontend dashboards, AI integration, and deployment architecture.

## ☁️ Production Deployment

The project is fully deployed online using Render and Streamlit Cloud.

## 📊 Interactive Visualization

Provides clear analytics dashboards for attack monitoring and threat insights.

## 🏅 Hackathon-Winning Architecture

Built with scalability, presentation quality, and production-level structure in mind.

---

# 👩‍💻 setty bhavana
---

# ⭐ Support The Project

If you found this project useful:

```text
⭐ Star the Repository
🍴 Fork the Project
🚀 Contribute Enhancements
```

---

# 🔮 Future Enhancements

* Real-Time Log Streaming
* SIEM Integration
* Kubernetes Deployment
* Role-Based Authentication
* AI Threat Forecasting
* Multi-User Security Dashboard
* Live Attack Simulation

---

# 📜 License

Licensed under the MIT License.

---

<p align="center">
  <h3>🛡️ Detect Faster • Analyze Smarter • Secure Better</h3>
</p>
