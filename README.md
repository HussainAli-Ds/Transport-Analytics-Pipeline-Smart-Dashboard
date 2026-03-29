# 🚛 Transport Analytics Pipeline & Dashboard

## 📊 Overview

This project is a complete **end-to-end data engineering + analytics solution**.

It automatically:

* 📂 Detects new Excel files
* 🧹 Cleans and transforms data
* 🗄️ Loads into PostgreSQL
* 📊 Displays insights in a professional Streamlit dashboard

---

## ⚡ Features

### 🔄 Data Pipeline

* Auto file detection (watch folder)
* Data cleaning & validation
* Handles missing & incorrect values
* Duplicate prevention using `ON CONFLICT`
* Fast bulk insert into PostgreSQL

---

### 📊 Dashboard (Streamlit)

* ✅ KPI Cards (Trips, Tons, Top Transporter, Top Material)
* 📈 Interactive charts
* 📍 Location-based analytics
* 📋 Transporter summary (Excel-style grouped view)
* 📦 Material summary
* 🔍 Advanced filters:

  * Date range
  * Transporter
  * Location
  * Material
* 📤 Export options:

  * Download filtered data (CSV)
  * Export summary (Excel)
* 🖨️ Print-ready dashboard
* 🎯 Clean & professional UI

---

## 🏗️ Tech Stack

* **Python**
* **Pandas**
* **SQLAlchemy**
* **PostgreSQL**
* **Streamlit**

---

## 📁 Project Structure

```
Pipeline-Transportor/
│
├── input_files/        # Excel files (input)
├── processed/          # Processed files
├── src/
│   ├── main.py         # Pipeline entry point
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── config.py
│
├── dashboard/
│   └── dashboard.py    # Streamlit dashboard
│
├── run_pipeline.bat
├── run_dashboard.bat
└── run_all.bat
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install pandas sqlalchemy psycopg2 streamlit openpyxl
```

---

### 2️⃣ Configure Database

Edit `config.py`:

```python
DB_URL = "postgresql+psycopg2://username:password@localhost:5432/db_name"
```

---

### 3️⃣ Run Pipeline

```bash
run_pipeline.bat
```

---

### 4️⃣ Run Dashboard

```bash
run_dashboard.bat
```

OR

```bash
streamlit run dashboard/dashboard.py
```

---

## 📊 Dashboard Preview
![Dashboard Preview](dashboard_pipeline.png)

### 🔹 KPI Cards

* Total Trips
* Total Tons
* Top Transporter
* Most Used Material

### 🔹 Analytics

* Trips by Transporter
* Tons by Material
* Location performance

### 🔹 Summary View

* Transporter-wise grouped data
* Material-wise totals
* Grand totals

---

## 💡 Advanced Features

* 📅 Smart date filtering
* 📍 Location filtering
* 🔄 Real-time updates
* 📤 Excel export
* 🖨️ Print-ready reports

---

## 🎯 Future Improvements

* Power BI style visuals
* Predictive analytics (ML)
* User authentication
* Cloud deployment (AWS / Azure)
* API integration

---

## 👨‍💻 Author

**Hussain Ali**
📧 [ha780383@gmail.com](mailto:ha780383@gmail.com)
📞 03357897412 | 03318782469

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
