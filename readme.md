## How to setup and configure project. 
---

### Prerequisites (WSL/Linux Only)
The app uses WeasyPrint for PDF generation, which requires system dependencies. Install them first:

```bash
sudo apt-get update
sudo apt-get install libpango-1.0-0 libpango1.0-dev libcairo2 libcairo2-dev
```

### Setup Instructions

#### 1. Create a virtual environment
```bash
python -m venv venv
```

#### 2. Activate virtual environment
```bash
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

#### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the application
```bash
streamlit run Dashboard.py
```

---

**Note:** This project is configured for WSL/Linux. System packages listed in `packages.txt` are required for WeasyPrint to generate PDFs properly.

