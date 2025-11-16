# How to Use Your JSON Format

## ✅ Your JSON Format is Ready!

I've created a wrapper that accepts **your exact JSON format** directly. No changes needed!

---

## 🚀 Quick Start (3 Steps)

### Step 1: Open the test file

```bash
cd "/Users/shrey/Backend optimisation - hack"
open test_your_json.py
# or: code test_your_json.py
```

### Step 2: Paste your JSON

Find this section in the file:

```python
# PASTE YOUR JSON HERE
your_json = {
    "loadConfig": {
        "type": "commercial",
        "subType": "",
        "sizeMW": 500,
        "carbonEmissions": 70,
        "onSiteGeneration": "yes",
        "configurationType": "battery"
    },
    "location": {
        "mode": "states",
        "selectedStates": ["Wisconsin", "Nebraska"],
        "selectedPoints": []
    }
}
```

Replace with your JSON!

### Step 3: Run it

```bash
python test_your_json.py
```

**Done!** Results will show in terminal and export to `results.csv`

---

## 📊 What You Get

### 1. Simple Table View
```
Rank   Node                          State  Score    LMP       
1      OTP.NWPS                      WI     0.9048   $11.39    
2      ALTW.STORMLK2                 WI     0.8799   $14.32    
```

### 2. Detailed Top Node Info
```
Node: OTP.NWPS
Location: Polk, WI
Overall Score: 0.9048

Component Scores:
  Cost:        1.000  (lower energy cost is better)
  Emissions:   1.000  (cleaner is better)
  ...
```

### 3. Frontend-Ready JSON
```json
{
  "success": true,
  "totalResults": 3,
  "results": [
    {
      "node": "OTP.NWPS",
      "location": {
        "state": "WI",
        "latitude": 45.263554,
        "longitude": -92.42165
      },
      "scores": {
        "overall": 0.9048,
        "rank": 1
      }
    }
  ]
}
```

### 4. CSV Export
Full results automatically saved to `results.csv`

---

## 📝 Your JSON Format Reference

### States Mode
```json
{
  "loadConfig": {
    "type": "commercial",           // or "industrial", "datacenter"
    "subType": "",                  // "continuous_process", "flexible", etc.
    "sizeMW": 500,                  // Load size
    "carbonEmissions": 70,          // 0-100 (sensitivity)
    "onSiteGeneration": "yes",      // "yes" or "no"
    "configurationType": "battery"  // "solar", "battery", "solar_battery", "firm_gen"
  },
  "location": {
    "mode": "states",
    "selectedStates": ["Wisconsin", "Nebraska"],  // Full state names
    "selectedPoints": []
  }
}
```

### Points Mode (100km radius per point)
```json
{
  "loadConfig": { ... },
  "location": {
    "mode": "points",
    "selectedStates": [],
    "selectedPoints": [
      {
        "id": "point-1763264891452",
        "lng": -108.72264303766178,
        "lat": 39.18291624575372
      },
      {
        "id": "point-1763264892236",
        "lng": -107.87709391027136,
        "lat": 41.76655632620444
      }
    ]
  }
}
```

---

## 🔄 How It Works

### Your JSON → Automatic Translation

| Your Field | Maps To | Notes |
|------------|---------|-------|
| `type: "commercial"` | `load_type: "commercial_campus"` | Auto-mapped |
| `type: "industrial"` + `subType: "continuous_process"` | `load_type: "industrial_continuous"` | Combined |
| `type: "datacenter"` + `subType: "flexible"` | `load_type: "data_center_flexible"` | Combined |
| `sizeMW` | `load_size_mw` | Direct |
| `carbonEmissions` | `emissions_preference` | Direct (0-100) |
| `onSiteGeneration: "yes"` + `configurationType: "battery"` | `resource_config: "battery"` | Combined |
| `selectedStates: ["Wisconsin"]` | `states: ["WI"]` | Full name → code |
| `selectedPoints` | 100km radius per point | Auto-handled |

---

## 🎯 Integration into Your App

### Option 1: Direct Python Integration

```python
from api_wrapper import rank_nodes_from_frontend_json, format_response_for_frontend

# Your JSON from frontend
frontend_json = { ... }

# Get results
results = rank_nodes_from_frontend_json(frontend_json, top_n=200)

# Format for frontend
response = format_response_for_frontend(results)

# Send back to frontend
return response
```

### Option 2: REST API

Update `api_server.py` to add a new endpoint:

```python
from api_wrapper import rank_nodes_from_frontend_json, format_response_for_frontend

@app.route("/api/rank_frontend", methods=["POST"])
def rank_frontend():
    frontend_json = request.get_json()
    results = rank_nodes_from_frontend_json(frontend_json, top_n=200)
    response = format_response_for_frontend(results)
    return jsonify(response)
```

Then call from frontend:
```javascript
const response = await fetch('/api/rank_frontend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(yourJson)
});
const data = await response.json();
```

---

## 🧪 Test Examples

### Example 1: Commercial Load in Multiple States

**File: `test_your_json.py`**

```python
your_json = {
    "loadConfig": {
        "type": "commercial",
        "subType": "",
        "sizeMW": 500,
        "carbonEmissions": 70,
        "onSiteGeneration": "yes",
        "configurationType": "battery"
    },
    "location": {
        "mode": "states",
        "selectedStates": ["Wisconsin", "Nebraska"],
        "selectedPoints": []
    }
}
```

Run: `python test_your_json.py`

---

### Example 2: Industrial Load Near Specific Points

**File: `test_your_json.py`**

```python
your_json = {
    "loadConfig": {
        "type": "industrial",
        "subType": "continuous_process",
        "sizeMW": 500,
        "carbonEmissions": 30,
        "onSiteGeneration": "yes",
        "configurationType": "battery"
    },
    "location": {
        "mode": "points",
        "selectedStates": [],
        "selectedPoints": [
            {
                "id": "point-1",
                "lng": -108.72,
                "lat": 39.18
            },
            {
                "id": "point-2",
                "lng": -107.88,
                "lat": 41.77
            }
        ]
    }
}
```

Run: `python test_your_json.py`

**Note:** For points mode, the system:
1. Searches 100km radius around each point
2. Combines results from all points
3. Removes duplicates (keeps best score)
4. Re-ranks combined results

---

## 📋 Load Type Mappings

| Your Input | System Maps To |
|------------|----------------|
| `"commercial"` | `commercial_campus` |
| `"datacenter"` or `"data center"` (no subtype) | `data_center_always_on` |
| `"datacenter"` + subType: `"flexible"` | `data_center_flexible` |
| `"industrial"` (no subtype) | `industrial_continuous` |
| `"industrial"` + subType: `"continuous_process"` | `industrial_continuous` |
| `"industrial"` + subType: `"flexible"` | `industrial_flexible` |
| `"hydrogen"` or `"h2"` or `"electrolyzer"` | `h2_electrolyzer_firm` |

---

## 🔧 Customization Options

### Change Number of Results

In `test_your_json.py`:
```python
results = rank_nodes_from_frontend_json(your_json, top_n=50)  # Get top 50
```

### Pre-load Data (for faster repeated calls)

```python
from node_ranking_engine import load_nodes_from_csv
from api_wrapper import rank_nodes_from_frontend_json

# Load once
nodes_df = load_nodes_from_csv("final_csv_v1.csv")

# Reuse for multiple queries
results1 = rank_nodes_from_frontend_json(json1, nodes_df=nodes_df, top_n=200)
results2 = rank_nodes_from_frontend_json(json2, nodes_df=nodes_df, top_n=200)
results3 = rank_nodes_from_frontend_json(json3, nodes_df=nodes_df, top_n=200)
```

---

## 🎨 Frontend Response Format

```json
{
  "success": true,
  "totalResults": 10,
  "results": [
    {
      "node": "OTP.NWPS",
      "location": {
        "state": "WI",
        "county": "Polk, WI",
        "latitude": 45.263554,
        "longitude": -92.42165,
        "iso": "MISO"
      },
      "scores": {
        "overall": 0.9048,
        "rank": 1,
        "components": {
          "cost": 1.0,
          "land": 0.5,
          "emissions": 1.0,
          "policy": 1.0,
          "queue": 1.0,
          "variability": 0.795
        }
      },
      "metrics": {
        "lmp": 11.39,
        "landPricePerAcre": 647.0,
        "emissionsIntensity": 0.0,
        "queuePendingMW": 0.0
      }
    }
  ]
}
```

**Easy to display in your UI!**

---

## 🐛 Troubleshooting

### "Unknown state name"

**Issue:** State name not recognized

**Fix:** Check spelling. Supported formats:
- Full name: "Wisconsin", "California"
- Abbreviation: "WI", "CA" (auto-detected)

---

### "No results returned"

**Issue:** No nodes in selected area

**Fix:** 
- For states: Try adding more states
- For points: Increase radius (currently 100km fixed, can change in `api_wrapper.py`)

---

### Different results than expected

**Issue:** Weights might not match your expectations

**Fix:** Check the weight breakdown in output. Adjust `carbonEmissions` value:
- 0-30: Low emissions focus
- 30-70: Moderate
- 70-100: High emissions focus

---

## 📞 Quick Reference

```bash
# Test with your JSON
cd "/Users/shrey/Backend optimisation - hack"
open test_your_json.py    # Edit the your_json variable
python test_your_json.py  # Run

# Files you need:
# - api_wrapper.py         (handles your JSON format)
# - test_your_json.py      (test script)
# - node_ranking_engine.py (core engine)
# - final_csv_v1.csv       (data)
```

---

## 🚀 Ready to Use!

**Your JSON format works exactly as-is. Just:**

1. Edit `test_your_json.py`
2. Paste your JSON
3. Run `python test_your_json.py`

**For production integration:**

```python
from api_wrapper import rank_nodes_from_frontend_json, format_response_for_frontend

results = rank_nodes_from_frontend_json(your_frontend_json, top_n=200)
response = format_response_for_frontend(results)
# Send response to frontend
```

---

**Need help? All the code is ready to go! Just run:**

```bash
python test_your_json.py
```

🎉

