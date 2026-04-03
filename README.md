# 💊 Pharmacy Management System – Microservices Architecture

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Microservices-green)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 Project Description

The **Pharmacy Management System** is a scalable, modern system designed to manage **customers, suppliers, medicines, prescriptions, inventory, orders, and payments** in a pharmacy environment.  
It is built with **FastAPI** for backend microservices and **MongoDB** for data storage, following a **microservices architecture** to ensure modularity, scalability, and maintainability.

This project also includes a **central API Gateway** to route client requests to the appropriate services seamlessly.

---

## 🚀 Features

- ✅ Modular microservices for each domain (Customer, Supplier, Medicine, etc.)
- ✅ Centralized API Gateway for routing requests
- ✅ MongoDB integration with environment-based configuration
- ✅ Swagger UI documentation for each microservice
- ✅ Loosely coupled services for easy scaling and maintenance
- ✅ Ready for Dockerization and cloud deployment

---

## 🔧 Microservices Overview

| Service              | Port | Description                  |
|----------------------|------|------------------------------|
| 👤 Customer Service  | 8001 | Manage customer data         |
| 🚚 Supplier Service  | 8002 | Handle supplier operations   |
| 💊 Medicine Service  | 8003 | Manage medicines             |
| 📦 Inventory Service | 8004 | Track stock & availability   |
| 📄 Prescription Service | 8005 | Manage prescriptions         |
| 🛒 Order Service     | 8006 | Handle orders                |
| 💳 Payment Service   | 8007 | Process payments             |
| 🌐 API Gateway       | 8000 | Central request routing      |
| 👤 User Service  | 8008 | Manage User data         |

---

## 🏛️ Architecture

- 🔄 Requests go through **API Gateway**
- 🔗 Services are **independent and loosely coupled**
- 🗄️ Each service maintains its **own database connection**

---

## ⚙️ Prerequisites

- 🐍 Python `3.10+` (Recommended: `3.12`)
- 🍃 MongoDB (Local or Atlas)
- 📚 Git

---

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repository-url>
   cd pharmacy-microservices
   ```

2. **Create Virtual Environment:**

   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔐 Environment Configuration

Create `.env` files in each service directory:

- `Customer_Service/.env`
- `Supplier_Service/.env`
- `Medicine_Service/.env`
- `Inventory_Service/.env`
- `Prescription_Service/.env`
- `Order_Service/.env`
- `Payment_Service/.env`
- `Auth_Service/.env`

Add the following to each `.env` file:

```env
MONGO_URL="your mongodb url"
```

---

## ▶️ Running the Services

Start each microservice in separate terminals:

1. **Customer Service:**
   ```bash
   cd Customer_Service
   python main.py
   ```

2. **Supplier Service:**
   ```bash
   cd Supplier_Service
   python main.py
   ```

3. **Medicine Service:**
   ```bash
   cd Medicine_Service
   python main.py
   ```

4. **Inventory Service:**
   ```bash
   cd Inventory_Service
   python main.py
   ```

5. **Prescription Service:**
   ```bash
   cd Prescription_Service
   python main.py
   ```

6. **Order Service:**
   ```bash
   cd Order_Service
   python main.py
   ```

7. **Payment Service:**
   ```bash
   cd Payment_Service
   python main.py
   ```

8. **API Gateway:**
   ```bash
   cd Gateway
   python main.py
   ```

---

## 📄 API Documentation (Swagger UI)

| Service              | URL                          |
|----------------------|------------------------------|
| 🌐 Gateway           | http://127.0.0.1:8000/docs   |
| 👤 Customer          | http://127.0.0.1:8001/docs   |
| 🚚 Supplier          | http://127.0.0.1:8002/docs   |
| 💊 Medicine          | http://127.0.0.1:8003/docs   |
| 📦 Inventory         | http://127.0.0.1:8004/docs   |
| 📄 Prescription      | http://127.0.0.1:8005/docs   |
| 🛒 Order             | http://127.0.0.1:8006/docs   |
| 💳 Payment           | http://127.0.0.1:8007/docs   |
| 👤 Auth         | http://127.0.0.1:8008/docs   |

---

## 🧪 Testing

You can test APIs using:

- 🔗 **Swagger UI** (`/docs`)
- 📮 **Postman**
- ⚡ **Thunder Client** (VS Code)

---

## ⚠️ Important Notes

- 🚀 Start all microservices before using the Gateway
- ⚙️ Gateway routes are configured in `Gateway/main.py`
- 🗄️ Ensure MongoDB is running before starting services

---

## 🤝 How to Contribute

We welcome contributions from everyone. Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and add tests.
4. Commit your changes: `git commit -m "feat: add your feature"`.
5. Push to your fork: `git push origin feature/your-feature-name`.
6. Open a Pull Request and describe what you changed.

### 🧾 Contribution Guide Table

| Type | Checklist | Notes |
|------|-----------|-------|
| Bugfix | ✅ Reproduced issue locally<br>✅ Added failing test<br>✅ Verified fix | Ensure issue is linked in PR |
| New Feature | ✅ Proposal created<br>✅ Implementation complete<br>✅ Documentation updated | Include API contract updates if any |
| Refactor | ✅ Behavior unchanged<br>✅ Tests pass | Keep changes small and clear |

---

## 👨‍💻 Contributors

| IT Number  | Name           | Contribution                          |
|------------|----------------|---------------------------------------|
| IT22569318  | Oshan Lahiru  | Customer Service, Order Service, Auth Service API Development     |
| IT22570758  | Heshani Niwanthika      | Medicine Services         |
| IT22564122  | Buddhika Roshan    | Payment Services      |
| IT22592088  | Sonali Liyanahetti    | Prescription Services              |
| IT22586902  | Shamith Udesha     | Supplier Services             |
| IT22576248  | Kavindya Kalahewatte     | Inventory Services             |

---

## 🌟 Future Improvements

- 🔐 Centralized Authentication (JWT / OAuth2)
- 🐳 Docker & Kubernetes Deployment
- 📊 Monitoring (Prometheus + Grafana)
- 🔄 CI/CD Pipeline (GitHub Actions)
- 🤖 Add AI-based inventory prediction and analytics