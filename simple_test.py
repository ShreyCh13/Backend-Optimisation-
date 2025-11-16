"""
Simple Test Interface - Quick Parameter Testing

The fastest way to test different parameter combinations.
Just edit the test_configs list and run!

Usage: python simple_test.py
"""

from node_ranking_engine import rank_nodes, load_nodes_from_csv


# ============================================================================
# EDIT THESE CONFIGURATIONS TO TEST DIFFERENT SCENARIOS
# ============================================================================

test_configs = [
    {
        "name": "Test 1: CA Data Center with Solar+Battery",
        "load_type": "data_center_always_on",
        "load_size_mw": 600,
        "location_filter": {"states": ["CA"]},
        "emissions_preference": 80,
        "resource_config": "solar_battery",
        "top_n": 8
    },
    {
        "name": "Test 2: National H2 Search (High Emissions Focus)",
        "load_type": "data_center_always_on",
        "load_size_mw": 100,
        "location_filter": {"states": ["CA"]},
        "emissions_preference": 90,
        "resource_config": "none",
        "top_n": 5
    },
    {
        "name": "Test 3: TX Industrial with Battery",
        "load_type": "industrial_continuous",
        "load_size_mw": 75,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 30,
        "resource_config": "battery",
        "top_n": 5
    },
    # ADD YOUR OWN TESTS HERE:
    # {
    #     "name": "My Custom Test",
    #     "load_type": "data_center_flexible",
    #     "load_size_mw": 150,
    #     "location_filter": {"states": ["NY", "NJ"]},
    #     "emissions_preference": 60,
    #     "resource_config": "solar",
    #     "top_n": 10
    # },
]


# ============================================================================
# DON'T EDIT BELOW THIS LINE (unless you want to customize output format)
# ============================================================================

def print_results(name, results):
    """Print results in a clean format."""
    print("\n" + "="*80)
    print(f"  {name}")
    print("="*80)
    
    if len(results) == 0:
        print("  ✗ No results returned")
        return
    
    print(f"\n  Results: {len(results)} nodes")
    print(f"  Top Node: {results.iloc[0]['node']}")
    print(f"  Top Score: {results.iloc[0]['score_scenario']:.4f}")
    
    print(f"\n  {'Rank':<6} {'Node':<40} {'State':<6} {'Score':<8} {'LMP':<10}")
    print(f"  {'-'*6} {'-'*40} {'-'*6} {'-'*8} {'-'*10}")
    
    for idx, row in results.iterrows():
        rank = int(row['rank_scenario'])
        node = str(row['node'])[:38]
        state = str(row['state'])
        score = row['score_scenario']
        lmp = row['avg_lmp']
        print(f"  {rank:<6} {node:<40} {state:<6} {score:<8.4f} ${lmp:<9.2f}")
    
    # Component scores for top node
    top = results.iloc[0]
    print(f"\n  Component Scores (Top Node):")
    print(f"    Cost:      {top['cost_score']:.3f}")
    print(f"    Land:      {top['land_score']:.3f}")
    print(f"    Emissions: {top['emissions_score']:.3f}")
    print(f"    Policy:    {top['policy_score']:.3f}")
    print(f"    Queue:     {top['queue_score']:.3f}")
    print(f"    Variabil:  {top['effective_price_variability_penalty_score']:.3f}")


def main():
    """Run all test configurations."""
    print("\n" + "="*80)
    print("  NODE RANKING ENGINE - SIMPLE TEST RUNNER")
    print("="*80)
    
    # Load data once
    print("\n  Loading data...")
    try:
        nodes_df = load_nodes_from_csv("final_csv_v1.csv")
        print(f"  ✓ Loaded {len(nodes_df):,} nodes")
    except Exception as e:
        print(f"  ✗ Failed to load data: {e}")
        return
    
    # Run each test
    print(f"\n  Running {len(test_configs)} test(s)...")
    
    for i, config in enumerate(test_configs, 1):
        test_name = config.pop("name", f"Test {i}")
        
        print(f"\n  [{i}/{len(test_configs)}] {test_name}...")
        
        try:
            results = rank_nodes(nodes_df=nodes_df, **config)
            print_results(test_name, results)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Re-add name for next iteration if running in loop
        config["name"] = test_name
    
    print("\n" + "="*80)
    print("  All tests completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

