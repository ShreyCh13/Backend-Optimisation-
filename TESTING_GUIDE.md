# Testing Guide for Node Ranking Engine

Quick guide to test the ranking engine with different inputs using the provided test interfaces.

---

## 🎯 Two Testing Interfaces

### 1. **Interactive Test Interface** (Recommended for exploration)
**File**: `interactive_test.py`

A full interactive CLI that walks you through all parameters with menus and validation.

```bash
python interactive_test.py
```

**Features:**
- ✅ Menu-driven parameter selection
- ✅ Input validation with helpful error messages
- ✅ Weight breakdown visualization
- ✅ Predefined quick scenarios
- ✅ Export results to CSV
- ✅ Colorized output for readability

**Perfect for:**
- Learning the system
- Exploring different parameters
- Understanding weight impacts
- One-off testing

---

### 2. **Simple Test Runner** (Recommended for quick testing)
**File**: `simple_test.py`

Edit test configurations in the file, then run all tests at once.

```bash
python simple_test.py
```

**Features:**
- ✅ Edit configs directly in the file
- ✅ Run multiple tests in one go
- ✅ Clean, compact output
- ✅ Fast iteration

**Perfect for:**
- Running multiple scenarios quickly
- Comparing different configurations
- Batch testing
- Automated testing

---

## 🚀 Quick Start

### Option A: Interactive Testing

```bash
python interactive_test.py
```

Then select:
- Option 1: Custom test (configure everything)
- Option 2: Quick scenarios (predefined tests)

**Example Session:**

```
1. Select load type: data_center_always_on
2. Enter load size: 250 MW
3. Location filter: States → CA
4. Emissions preference: 80
5. Resource config: solar_battery
6. Top N: 10

→ View results with component scores
→ Export to CSV if needed
```

---

### Option B: Simple Testing

1. **Edit `simple_test.py`**:

```python
test_configs = [
    {
        "name": "My Test: CA Data Center",
        "load_type": "data_center_always_on",
        "load_size_mw": 250,
        "location_filter": {"states": ["CA"]},
        "emissions_preference": 80,
        "resource_config": "solar_battery",
        "top_n": 10
    },
    # Add more tests here...
]
```

2. **Run it**:

```bash
python simple_test.py
```

---

## 📝 Parameter Reference

### Load Types

```python
"data_center_always_on"      # Constant 24/7 load
"data_center_flexible"       # Interruptible load
"h2_electrolyzer_firm"       # Hydrogen production
"industrial_continuous"      # 24/7 industrial process
"industrial_flexible"        # Flexible industrial
"commercial_campus"          # Office/retail campus
```

### Location Filters

```python
# No filter (search all locations)
"location_filter": None

# State-based filter
"location_filter": {"states": ["CA", "NY", "TX"]}

# Radial search (within radius of a point)
"location_filter": {
    "lat": 37.77,        # San Francisco
    "lon": -122.42,
    "radius_km": 200
}
```

### Resource Configurations

```python
"none"            # Grid-only (0% variability reduction)
"solar"           # On-site solar (30% reduction)
"battery"         # Battery storage (40% reduction)
"solar_battery"   # Solar + battery (60% reduction)
"firm_gen"        # Firm generation (75% reduction)
```

### Emissions Preference

```python
0-20    # Don't care
20-40   # Somewhat care
40-60   # Moderately care
60-80   # Strongly care
80-100  # Extremely sensitive
```

---

## 💡 Common Test Scenarios

### Test 1: Compare Resource Scenarios

**Use simple_test.py:**

```python
test_configs = [
    {
        "name": "Scenario 1: Grid Only",
        "load_type": "data_center_always_on",
        "load_size_mw": 200,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 50,
        "resource_config": "none",
        "top_n": 5
    },
    {
        "name": "Scenario 2: With Solar",
        "load_type": "data_center_always_on",
        "load_size_mw": 200,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 50,
        "resource_config": "solar",
        "top_n": 5
    },
    {
        "name": "Scenario 3: Solar + Battery",
        "load_type": "data_center_always_on",
        "load_size_mw": 200,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 50,
        "resource_config": "solar_battery",
        "top_n": 5
    }
]
```

---

### Test 2: Compare Load Types

```python
test_configs = [
    {
        "name": "Data Center",
        "load_type": "data_center_always_on",
        "load_size_mw": 100,
        "location_filter": None,
        "emissions_preference": 50,
        "resource_config": "none",
        "top_n": 3
    },
    {
        "name": "H2 Electrolyzer",
        "load_type": "h2_electrolyzer_firm",
        "load_size_mw": 100,
        "location_filter": None,
        "emissions_preference": 50,
        "resource_config": "none",
        "top_n": 3
    },
    {
        "name": "Industrial",
        "load_type": "industrial_continuous",
        "load_size_mw": 100,
        "location_filter": None,
        "emissions_preference": 50,
        "resource_config": "none",
        "top_n": 3
    }
]
```

---

### Test 3: Emissions Sensitivity

```python
test_configs = [
    {
        "name": "Low Emissions Sensitivity (20)",
        "load_type": "data_center_always_on",
        "load_size_mw": 150,
        "location_filter": {"states": ["CA", "TX"]},
        "emissions_preference": 20,
        "resource_config": "solar",
        "top_n": 3
    },
    {
        "name": "Medium Emissions Sensitivity (50)",
        "load_type": "data_center_always_on",
        "load_size_mw": 150,
        "location_filter": {"states": ["CA", "TX"]},
        "emissions_preference": 50,
        "resource_config": "solar",
        "top_n": 3
    },
    {
        "name": "High Emissions Sensitivity (90)",
        "load_type": "data_center_always_on",
        "load_size_mw": 150,
        "location_filter": {"states": ["CA", "TX"]},
        "emissions_preference": 90,
        "resource_config": "solar",
        "top_n": 3
    }
]
```

---

### Test 4: Geographic Comparison

```python
test_configs = [
    {
        "name": "West Coast",
        "load_type": "industrial_flexible",
        "load_size_mw": 100,
        "location_filter": {"states": ["CA", "OR", "WA"]},
        "emissions_preference": 60,
        "resource_config": "battery",
        "top_n": 5
    },
    {
        "name": "Texas",
        "load_type": "industrial_flexible",
        "load_size_mw": 100,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 60,
        "resource_config": "battery",
        "top_n": 5
    },
    {
        "name": "Northeast",
        "load_type": "industrial_flexible",
        "load_size_mw": 100,
        "location_filter": {"states": ["NY", "PA", "NJ"]},
        "emissions_preference": 60,
        "resource_config": "battery",
        "top_n": 5
    }
]
```

---

## 📊 Understanding Results

### Output Sections

1. **Summary**
   - Total results
   - Top node name
   - Top score

2. **Rankings Table**
   - Rank (1 = best)
   - Node identifier
   - State
   - ISO
   - Composite score
   - LMP ($/MWh)

3. **Component Scores** (for top node)
   - Cost Score (0-1, higher = lower cost)
   - Land Score (0-1, higher = cheaper land)
   - Emissions Score (0-1, higher = cleaner)
   - Policy Score (0-1, higher = better support)
   - Queue Score (0-1, higher = less congestion)
   - Variability Score (0-1, higher = more stable)

4. **Geographic Distribution** (optional)
   - Breakdown by state
   - Percentage of results

---

## 🎨 Interactive Interface Features

### Menu Navigation

```
MAIN MENU
---------
1. Custom ranking test (configure all parameters)
2. Quick scenario tests (predefined scenarios)
3. Exit
```

### Quick Scenarios

Pre-configured tests for common use cases:
1. CA Data Center (250 MW, high emissions)
2. National H2 Electrolyzer (100 MW)
3. TX Industrial (75 MW, cost-focused)
4. Multi-state flexible data center
5. Run all scenarios

### Weight Visualization

```
Component weights for your configuration:
  cost         0.1960 █████████
  land         0.1851 █████████
  policy       0.1307 ██████
  queue        0.1525 ███████
  emissions    0.2036 ██████████
  variability  0.1321 ██████
```

---

## 🔧 Tips & Tricks

### Tip 1: Start with Quick Scenarios
Use interactive interface → Option 2 to see predefined examples first.

### Tip 2: Use Simple Test for Comparisons
When comparing multiple scenarios, edit `simple_test.py` and run all at once.

### Tip 3: Export Results
In interactive mode, you can export results to CSV for further analysis in Excel/Tableau.

### Tip 4: Check Component Scores
Always look at component scores to understand WHY a node ranked well.

### Tip 5: Test Edge Cases
- Try emissions_preference = 0 vs. 100
- Compare load_size_mw = 10 vs. 500
- Test both radial and state filters

---

## 🐛 Troubleshooting

### "No results returned"

**Cause**: Location filter too restrictive

**Fix**: 
- Widen the radius for radial search
- Add more states to state filter
- Set location_filter to None

### Unexpected results

**Cause**: Weight configuration

**Fix**: 
- Check weight breakdown (shown in interactive mode)
- Try different emissions_preference values
- Compare component scores

### Slow performance

**Cause**: Large search space

**Fix**:
- Use location_filter to narrow search
- Reduce top_n to what you actually need
- Run with fewer tests

---

## 📈 Example Workflow

### Workflow 1: Exploring a New Use Case

1. Run `python interactive_test.py`
2. Select Option 2 (Quick scenarios)
3. Run similar scenario to yours
4. Note the results
5. Select Option 1 (Custom test)
6. Adjust parameters based on insights
7. Export results

### Workflow 2: Comparing Multiple Scenarios

1. Edit `simple_test.py`
2. Add 3-5 test configurations
3. Run `python simple_test.py`
4. Compare results side-by-side
5. Iterate on parameters

### Workflow 3: Integration Testing

1. Use simple_test.py as template
2. Replace with your application's parameters
3. Verify results match expectations
4. Integrate rank_nodes() into your app

---

## 🎯 Next Steps

After testing with these interfaces:

1. **For developers**: Integrate `rank_nodes()` directly into your application
2. **For API users**: Use `api_server.py` for REST API access
3. **For researchers**: Export results and analyze in detail
4. **For product**: Provide feedback on weight calibration

---

## 📞 Quick Reference

```bash
# Interactive testing (menu-driven)
python interactive_test.py

# Simple batch testing (edit configs in file)
python simple_test.py

# Full test suite (validation)
python test_ranking_engine.py

# Comprehensive demos (learning)
python demo_ranking.py

# Quick examples (copy-paste)
python quick_start.py

# API server (REST interface)
python api_server.py
```

---

**Ready to test? Start with:**

```bash
python interactive_test.py
```

**For quick iteration:**

```bash
python simple_test.py
```

Happy testing! 🚀

