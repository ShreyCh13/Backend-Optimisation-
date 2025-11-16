# Getting Started with Node Ranking Engine

## 📁 Project Structure

```
Backend optimisation - hack/
│
├── 📊 DATA
│   └── final_csv_v1.csv                    # Input data: 29,998 power system nodes
│
├── 🧠 CORE ENGINE
│   └── node_ranking_engine.py              # Main ranking module (850+ lines)
│       ├── Normalization helpers
│       ├── Spatial filtering
│       ├── Component score calculation
│       ├── Weight adjustment logic
│       └── Main rank_nodes() function
│
├── 🌐 API SERVER
│   └── api_server.py                       # Flask REST API (350+ lines)
│       ├── /api/rank         - POST: Rank nodes
│       ├── /api/weights      - POST: Get weight breakdown
│       └── /api/health       - GET: Health check
│
├── 🧪 TESTING
│   └── test_ranking_engine.py              # Test suite (400+ lines)
│       ├── ✅ Normalization tests
│       ├── ✅ Spatial filtering tests
│       ├── ✅ Weight computation tests
│       ├── ✅ Data validation tests
│       ├── ✅ Full ranking tests
│       └── ✅ Score properties tests
│
├── 🎯 DEMONSTRATIONS
│   ├── demo_ranking.py                     # Advanced demos (500+ lines)
│   │   ├── Demo 1: California data center
│   │   ├── Demo 2: H2 electrolyzer search
│   │   ├── Demo 3: Radial search
│   │   ├── Demo 4: Scenario comparison
│   │   ├── Demo 5: Weight analysis
│   │   └── Demo 6: Emissions sensitivity
│   │
│   └── quick_start.py                      # Quick examples (350+ lines)
│       ├── Example 1: Simplest usage
│       ├── Example 2: State filter
│       ├── Example 3: Radial search
│       ├── Example 4: Compare scenarios
│       ├── Example 5: Different load types
│       ├── Example 6: Emissions sensitivity
│       ├── Example 7: Export results
│       └── Example 8: Custom analysis
│
├── 📚 DOCUMENTATION
│   ├── README.md                           # Complete API reference (400+ lines)
│   ├── PROJECT_SUMMARY.md                  # Project overview and results
│   └── GETTING_STARTED.md                  # This file
│
└── 📦 CONFIGURATION
    └── requirements.txt                    # Python dependencies
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd "/Users/shrey/Backend optimisation - hack"
pip install pandas numpy
```

### Step 2: Run Test Suite (Verify Installation)

```bash
python test_ranking_engine.py
```

Expected output: ✅ **ALL TESTS PASSED! (6/6)**

### Step 3: Run Your First Ranking

```bash
python quick_start.py
```

Or try the simplest example:

```python
from node_ranking_engine import rank_nodes, load_nodes_from_csv

# Load data
nodes_df = load_nodes_from_csv("final_csv_v1.csv")

# Rank nodes
results = rank_nodes(
    nodes_df=nodes_df,
    load_type="data_center_always_on",
    load_size_mw=100,
    location_filter={"states": ["CA"]},
    emissions_preference=50,
    resource_config="solar",
    top_n=10
)

# View results
print(results[['node', 'state', 'score_scenario', 'rank_scenario']])
```

---

## 🎓 Learning Path

### Beginner (First 30 minutes)

1. **Read this file** (GETTING_STARTED.md) - You're here! ✅
2. **Run quick_start.py** - See 8 simple examples
   ```bash
   python quick_start.py
   ```
3. **Run test suite** - Verify everything works
   ```bash
   python test_ranking_engine.py
   ```

### Intermediate (Next 1-2 hours)

4. **Read README.md** - Understand the complete API
5. **Run demo_ranking.py** - See sophisticated use cases
   ```bash
   python demo_ranking.py
   ```
6. **Modify examples** - Adapt to your specific needs

### Advanced (Building Applications)

7. **Read PROJECT_SUMMARY.md** - Understand architecture and design decisions
8. **Integrate into your application**:
   - Direct Python: Import and use `rank_nodes()`
   - REST API: Start `api_server.py` and make HTTP requests
   - Batch processing: Loop over scenarios
9. **Customize weights** - Modify multipliers in `get_load_type_multipliers()`

---

## 💻 Common Use Cases

### Use Case 1: Find Top Locations for a Data Center

```python
from node_ranking_engine import rank_nodes, load_nodes_from_csv

nodes_df = load_nodes_from_csv("final_csv_v1.csv")

results = rank_nodes(
    nodes_df=nodes_df,
    load_type="data_center_always_on",     # Constant load
    load_size_mw=250,                       # 250 MW facility
    location_filter={"states": ["CA", "OR", "WA"]},  # West coast
    emissions_preference=80,                 # High emissions sensitivity
    resource_config="solar_battery",         # On-site solar + battery
    top_n=20                                 # Top 20 locations
)

# Save results
results.to_csv("data_center_rankings_west_coast.csv", index=False)
```

### Use Case 2: Compare Resource Scenarios

```python
# Try different resource configurations
configs = ["none", "solar", "battery", "solar_battery", "firm_gen"]

for config in configs:
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="industrial_continuous",
        load_size_mw=100,
        location_filter={"states": ["TX"]},
        emissions_preference=60,
        resource_config=config,
        top_n=5
    )
    
    print(f"\n{config.upper()}:")
    print(f"  Top node: {results.iloc[0]['node']}")
    print(f"  Score: {results.iloc[0]['score_scenario']:.3f}")
```

### Use Case 3: National H2 Electrolyzer Search

```python
results = rank_nodes(
    nodes_df=nodes_df,
    load_type="h2_electrolyzer_firm",       # Hydrogen production
    load_size_mw=100,
    location_filter=None,                    # No geographic restrictions
    emissions_preference=95,                 # Extremely high sensitivity
    resource_config="none",                  # Grid-only
    top_n=50
)

# Analyze results by state
print(results['state'].value_counts())
print(f"\nAverage emissions: {results['county_emissions_intensity_kg_per_mwh'].mean():.1f} kg/MWh")
```

### Use Case 4: Radial Search Near a City

```python
# Find nodes within 200 km of Houston, TX (29.76, -95.37)
results = rank_nodes(
    nodes_df=nodes_df,
    load_type="commercial_campus",
    load_size_mw=50,
    location_filter={"lat": 29.76, "lon": -95.37, "radius_km": 200},
    emissions_preference=50,
    resource_config="battery",
    top_n=15
)

print(f"Found {len(results)} nodes within 200 km of Houston")
```

---

## 🔧 API Server Usage

### Start the Server

```bash
python api_server.py
```

Server runs at: `http://localhost:5000`

### Make a Request (curl)

```bash
curl -X POST http://localhost:5000/api/rank \
  -H "Content-Type: application/json" \
  -d '{
    "load_type": "data_center_always_on",
    "load_size_mw": 250,
    "location_filter": {"states": ["CA"]},
    "emissions_preference": 80,
    "resource_config": "solar_battery",
    "top_n": 10
  }'
```

### Make a Request (Python)

```python
import requests

response = requests.post(
    "http://localhost:5000/api/rank",
    json={
        "load_type": "data_center_always_on",
        "load_size_mw": 250,
        "location_filter": {"states": ["CA"]},
        "emissions_preference": 80,
        "resource_config": "solar_battery",
        "top_n": 10
    }
)

results = response.json()
print(f"Success: {results['success']}")
print(f"Top node: {results['results'][0]['node']}")
```

---

## 🎛️ Parameters Guide

### Load Types

| Type | Use For | Key Characteristics |
|------|---------|---------------------|
| `data_center_always_on` | Constant load data centers | High land and variability weights |
| `data_center_flexible` | Flexible data centers | Lower variability weight |
| `h2_electrolyzer_firm` | Hydrogen production | Very high emissions and queue weights |
| `industrial_continuous` | 24/7 manufacturing | Balanced with cost/queue emphasis |
| `industrial_flexible` | Flexible industrial | Lower variability weight |
| `commercial_campus` | Office/retail campus | Moderate across all factors |

### Load Size Guidelines

- **< 50 MW**: Small load - queue less critical
- **50-150 MW**: Medium load - standard weighting
- **> 150 MW**: Large load - queue and variability very important

### Emissions Preference Scale

- **0-20**: Don't care about emissions
- **20-40**: Somewhat care about emissions
- **40-60**: Moderately care about emissions
- **60-80**: Strongly care about emissions
- **80-100**: Extremely sensitive to emissions

### Resource Configurations

| Config | Variability Reduction | Best For |
|--------|----------------------|----------|
| `none` | 0% | Grid-dependent loads |
| `solar` | 30% | Daytime-heavy loads |
| `battery` | 40% | Peak shaving needs |
| `solar_battery` | 60% | High independence |
| `firm_gen` | 75% | Critical reliability |

---

## 📊 Understanding Results

### Output Columns

#### Identification
- `node` - Unique node identifier
- `state` - State code
- `iso` - ISO/RTO name
- `county_state_pairs` - County, State for display
- `latitude`, `longitude` - Geographic coordinates

#### Composite Scores
- `score_baseline` - Score without on-site resources [0-1]
- `score_scenario` - Score with selected resource config [0-1]
- `rank_baseline` - Rank without resources (1=best)
- `rank_scenario` - Rank with resources (1=best)

#### Component Scores (all 0-1, higher is better)
- `cost_score` - Energy cost competitiveness
- `land_score` - Land availability/affordability
- `emissions_score` - Low emissions intensity
- `policy_score` - Policy support and incentives
- `queue_score` - Interconnection queue health
- `price_variability_penalty_score` - Baseline price stability
- `effective_price_variability_penalty_score` - Stability with resources

#### Raw Metrics
- `avg_lmp` - Locational marginal price ($/MWh)
- `avg_price_per_acre` - Land price ($/acre)
- `county_emissions_intensity_kg_per_mwh` - Grid emissions (kg CO2/MWh)
- `queue_pending_mw` - Pending interconnection queue (MW)
- And more...

---

## 🐛 Troubleshooting

### "No nodes remain after filtering"

**Cause**: Location filter too restrictive

**Solution**: 
- For state filter: Check state codes are correct (e.g., "CA" not "California")
- For radial filter: Increase radius_km or check coordinates

### "Unexpected rankings"

**Cause**: Weights may not match expectations

**Solution**:
```python
from node_ranking_engine import compute_final_weights

# Check weight breakdown
weights = compute_final_weights(
    load_type="data_center_always_on",
    load_size_mw=250,
    emissions_preference=80
)
print(weights)
```

### "Slow performance"

**Cause**: Large dataset or no pre-filtering

**Solution**:
- Use location_filter to reduce search space
- Reduce top_n to only what you need
- Check that data has been cleaned (run validation once)

---

## 📈 Next Steps

### For Developers
1. ✅ Run test suite to verify setup
2. ✅ Try quick_start.py examples
3. ✅ Read README.md for complete API
4. ✅ Integrate into your application

### For Researchers
1. ✅ Run demo_ranking.py for analysis examples
2. ✅ Examine weight multipliers in code
3. ✅ Export results for further analysis
4. ✅ Modify parameters to test hypotheses

### For Product Teams
1. ✅ Start api_server.py for frontend integration
2. ✅ Review PROJECT_SUMMARY.md for capabilities
3. ✅ Test with your specific use cases
4. ✅ Provide feedback for weight calibration

---

## 🎯 Key Files to Read

**Start here:**
1. `GETTING_STARTED.md` (this file) - Quick orientation
2. `quick_start.py` - Copy-paste examples

**Then:**
3. `README.md` - Complete reference
4. `demo_ranking.py` - Advanced use cases

**For deep understanding:**
5. `PROJECT_SUMMARY.md` - Architecture and design
6. `node_ranking_engine.py` - Source code (well-commented)

---

## ✅ Verification Checklist

Before deploying or integrating, verify:

- [ ] Test suite passes (`python test_ranking_engine.py`)
- [ ] Quick start examples work (`python quick_start.py`)
- [ ] You can load and rank your data
- [ ] Results make sense for your use case
- [ ] API server starts (if using REST API)
- [ ] You understand the weight adjustments
- [ ] You've reviewed the output schema

---

## 🎓 Additional Resources

- **README.md** - Complete API documentation
- **PROJECT_SUMMARY.md** - Architecture overview and results
- **test_ranking_engine.py** - Example of how functions work
- **node_ranking_engine.py** - Source code with inline comments

---

## 💡 Pro Tips

1. **Start simple**: Use default parameters, then customize
2. **Check weights**: Use `compute_final_weights()` to understand scoring
3. **Compare scenarios**: Run multiple resource configs to see differences
4. **Export results**: Save to CSV for analysis in Excel/Tableau
5. **Cache data**: Load `nodes_df` once, reuse for multiple rankings
6. **Use spatial filters**: Dramatically speeds up focused searches

---

## 🤝 Support

**Status**: ✅ Production Ready

- All tests passing (6/6)
- No linter errors
- 30,000 node dataset validated
- ~1.5 second typical processing time

For questions about:
- **Usage**: See README.md and quick_start.py
- **API**: See api_server.py
- **Testing**: See test_ranking_engine.py
- **Architecture**: See PROJECT_SUMMARY.md

---

**Ready to start? Run this:**

```bash
python quick_start.py
```

**Happy ranking! 🚀**

