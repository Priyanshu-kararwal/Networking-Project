# Enterprise Network Monitoring Project

## Setup & Deployment

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run the Streamlit app locally
```
streamlit run app.py
```

### 3. Deploy (Heroku example)
- Make sure you have a `Procfile` and `requirements.txt` in your project root.
- Push your code to Heroku or your preferred PaaS.

### 4. Network Topology Dashboard
To view the interactive network diagram, run:
```
python monitor.py
```

---

- All icons should be placed in the `icon/` folder.
- For production, ensure all dependencies are listed in `requirements.txt`.
