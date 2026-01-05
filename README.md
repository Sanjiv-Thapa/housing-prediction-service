# Housing Price Prediction Service 🏠

This project is a production-grade Machine Learning application designed to predict property values based on various house features. It demonstrates a complete end-to-end pipeline from raw data to a live web interface.

---

## 🚀 Key Project Milestones

* **Exploratory Data Analysis (EDA):** Analyzed the `Housing.csv` dataset to understand feature distributions and correlations.
* **XGBoost Model Development:** Built a regression model using Gradient Boosting, implementing log-transformations ($log1p$) to handle skewed price data and improve accuracy.
* **Database Evolution:** Successfully transitioned from flat-file CSV storage to a robust **PostgreSQL** relational database for better scalability and data integrity.
* **API Engineering:** Developed a **FastAPI** backend with automated Pydantic validation to handle requests and ensure high data quality.
* **Frontend Implementation:** Created a custom **HTML5/JavaScript** dashboard to allow users to interact with the model without needing technical API knowledge.

---

## 🛠️ Installation & Setup

### 1. Database Setup
* Install PostgreSQL and create a database named `housing_db`.
* Configure the connection string in `app/database.py`:
    ```python
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/housing_db"
    ```

### 2. Dependencies
Install the required libraries via terminal:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary xgboost scikit-learn pandas numpy python-multipart jinja2
🏗️ Project Structure
Plaintext

.
├── app/
│   ├── api/v1/predict.py   # Prediction logic and DB write operations
│   ├── models/db_models.py # SQLAlchemy database schema
│   ├── database.py         # Postgres connection management
│   └── main.py             # FastAPI entry point & static mounting
├── scripts/
│   ├── train.py            # Model training script
│   └── migrate_data.py     # CSV-to-SQL migration utility
├── static/
│   └── index.html          # Web frontend (HTML/JS)
├── models/
│   ├── house_model.json    # The trained XGBoost model file
│   └── model_metadata.json # Feature names and normalization stats
└── Housing.csv             # Original dataset