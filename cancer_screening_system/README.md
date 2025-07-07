# 🧠 Cancer Screening System

## 📌 Project Description

**Name**: Cancer Screening System  
**What it does**: Calculates cancer risk, determines screening intervals, and sends reminders.  
**Why it matters**: Helps automate preventive healthcare decisions and improves early cancer detection.

---

## 📁 Project Structure

cancer_screening_system/
│
├── data/ # Sample patient data (CSV)
├── models/ # Risk scoring logic
├── engine/ # Screening rules, scheduler, notification system
├── app/ # Main app pipeline
├── utils/ # Utility functions (e.g., date parsing)
├── README.md
└── requirements.txt
## ✨ Features

- ✅ Risk scoring based on age, lifestyle, and family history  
- ✅ Dynamic guideline engine (Strategy Pattern)  
- ✅ Screening schedule calculator  
- ✅ Notification system with multiple channels (console/log)  
- ✅ Optimized with caching and advanced data structures  

---

## 🛠️ Technologies Used

- **Python 3.10+**  
- Libraries: `pandas`, `datetime`, `enum`, `functools`  
- Design Patterns: Strategy, Singleton, Protocols, Enums  
- Optimizations: Memoization (`lru_cache`), DataClasses, Enums, Slots  

---

## 🚀 Installation

```bash
git clone <repo-url>
cd cancer_screening_system
pip install -r requirements.txt

How to Run
python app/main.py

 Sample Patient Data (patients.csv)
id,age,family_history,lifestyle,cancer_type,last_screening
1,55,True,smoker,breast,2020-07-01
2,45,False,healthy,cervical,2022-01-15
3,65,True,smoker,colorectal,2018-06-10

Author
Your Name – SHIVA CHARAN NEERUMAMIDI
