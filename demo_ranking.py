"""
Interactive demonstration of the Node Ranking Engine

This script shows various usage patterns and provides examples of how
the ranking engine can be integrated into a web API or UI.
"""

import pandas as pd
from node_ranking_engine import (
    rank_nodes,
    load_nodes_from_csv,
    get_ranking_explanation,
    compute_final_weights
)


def demo_1_california_datacenter():
    """Example: Large always-on data center in California with high emissions sensitivity."""
    print("\n" + "=" * 100)
    print("DEMO 1: Large Always-On Data Center in California")
    print("=" * 100)
    print("Scenario:")
    print("  - Load Type: Always-on data center")
    print("  - Size: 250 MW")
    print("  - Location: California only")
    print("  - Emissions Preference: 80/100 (very high)")
    print("  - Resource Config: Solar + Battery")
    print()
    
    # Load data
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Run ranking
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="data_center_always_on",
        load_size_mw=250,
        location_filter={"states": ["CA"]},
        emissions_preference=80,
        resource_config="solar_battery",
        top_n=20
    )
    
    # Display results
    print("\nTop 5 Ranked Nodes:")
    print("-" * 100)
    top5 = results.head(5)
    for idx, row in top5.iterrows():
        print(f"\nRank {row['rank_scenario']}: {row['node']}")
        print(f"  Location: {row['county_state_pairs']}, ISO: {row['iso']}")
        print(f"  Scenario Score: {row['score_scenario']:.4f} | Baseline Score: {row['score_baseline']:.4f}")
        print(f"  LMP: ${row['avg_lmp']:.2f}/MWh | Land: ${row['avg_price_per_acre']:.0f}/acre")
        print(f"  Component Scores:")
        print(f"    - Cost: {row['cost_score']:.3f}")
        print(f"    - Emissions: {row['emissions_score']:.3f}")
        print(f"    - Land: {row['land_score']:.3f}")
        print(f"    - Policy: {row['policy_score']:.3f}")
        print(f"    - Queue: {row['queue_score']:.3f}")
        print(f"    - Variability (scenario): {row['effective_price_variability_penalty_score']:.3f}")
    
    return results


def demo_2_flexible_electrolyzer():
    """Example: H2 electrolyzer with no location constraints."""
    print("\n" + "=" * 100)
    print("DEMO 2: H2 Electrolyzer - National Search")
    print("=" * 100)
    print("Scenario:")
    print("  - Load Type: Firm H2 electrolyzer")
    print("  - Size: 100 MW")
    print("  - Location: No restrictions (national)")
    print("  - Emissions Preference: 90/100 (extremely high)")
    print("  - Resource Config: None (grid-only)")
    print()
    
    # Load data
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Run ranking
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="h2_electrolyzer_firm",
        load_size_mw=100,
        location_filter=None,
        emissions_preference=90,
        resource_config="none",
        top_n=20
    )
    
    # Display results - focus on emissions and policy
    print("\nTop 5 Ranked Nodes:")
    print("-" * 100)
    top5 = results.head(5)
    for idx, row in top5.iterrows():
        print(f"\nRank {row['rank_scenario']}: {row['node']}")
        print(f"  Location: {row['state']}, ISO: {row['iso']}")
        print(f"  Scenario Score: {row['score_scenario']:.4f}")
        print(f"  Key Factors:")
        print(f"    - Emissions Intensity: {row['county_emissions_intensity_kg_per_mwh']:.1f} kg/MWh (Score: {row['emissions_score']:.3f})")
        print(f"    - Policy Support: {row['policy_score']:.3f}")
        print(f"    - Queue Pressure: {row['queue_score']:.3f}")
        print(f"    - LMP: ${row['avg_lmp']:.2f}/MWh")
    
    # Show geographic diversity
    print("\n\nGeographic Distribution of Top 20 Nodes:")
    print("-" * 100)
    state_counts = results['state'].value_counts()
    iso_counts = results['iso'].value_counts()
    print("\nBy State:")
    print(state_counts.to_string())
    print("\nBy ISO:")
    print(iso_counts.to_string())
    
    return results


def demo_3_radial_search():
    """Example: Industrial load near a specific location."""
    print("\n" + "=" * 100)
    print("DEMO 3: Industrial Load - Radial Search from Bay Area")
    print("=" * 100)
    print("Scenario:")
    print("  - Load Type: Industrial continuous")
    print("  - Size: 75 MW")
    print("  - Location: Within 200 km of San Francisco (37.77, -122.42)")
    print("  - Emissions Preference: 50/100 (moderate)")
    print("  - Resource Config: Battery storage")
    print()
    
    # Load data
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Run ranking with radial filter
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="industrial_continuous",
        load_size_mw=75,
        location_filter={"lat": 37.77, "lon": -122.42, "radius_km": 200},
        emissions_preference=50,
        resource_config="battery",
        top_n=15
    )
    
    # Display results
    print("\nTop 10 Ranked Nodes within 200 km:")
    print("-" * 100)
    top10 = results.head(10)
    
    # Calculate distance from center point
    from node_ranking_engine import haversine_distance_vectorized
    distances = haversine_distance_vectorized(37.77, -122.42, top10['latitude'], top10['longitude'])
    
    for idx, (row_idx, row) in enumerate(top10.iterrows()):
        print(f"\nRank {row['rank_scenario']}: {row['node']}")
        print(f"  Location: {row['county_state_pairs']}")
        print(f"  Distance from SF: {distances.iloc[idx]:.1f} km")
        print(f"  Score: {row['score_scenario']:.4f} | LMP: ${row['avg_lmp']:.2f}/MWh")
        print(f"  Cost Score: {row['cost_score']:.3f} | Queue Score: {row['queue_score']:.3f}")
    
    return results


def demo_4_scenario_comparison():
    """Example: Compare different resource configurations for the same load."""
    print("\n" + "=" * 100)
    print("DEMO 4: Resource Configuration Comparison")
    print("=" * 100)
    print("Scenario: Compare different on-site resource options for a flexible data center")
    print("  - Load Type: Flexible data center")
    print("  - Size: 150 MW")
    print("  - Location: Texas")
    print("  - Emissions Preference: 40/100")
    print()
    
    # Load data
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Common parameters
    common_params = {
        "nodes_df": nodes_df,
        "load_type": "data_center_flexible",
        "load_size_mw": 150,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 40,
        "top_n": 10
    }
    
    # Run ranking with different resource configs
    configs = ["none", "solar", "battery", "solar_battery", "firm_gen"]
    all_results = {}
    
    print("Running rankings for different resource configurations...\n")
    for config in configs:
        print(f"  - {config}")
        results = rank_nodes(**common_params, resource_config=config)
        all_results[config] = results
    
    # Compare top node across scenarios
    print("\n\nTop Node Across Different Resource Configurations:")
    print("-" * 100)
    print(f"{'Resource Config':<20} {'Top Node':<30} {'Score':<10} {'Variability Score':<18}")
    print("-" * 100)
    
    for config, results in all_results.items():
        if len(results) > 0:
            top_node = results.iloc[0]
            print(f"{config:<20} {top_node['node']:<30} {top_node['score_scenario']:.4f}     "
                  f"{top_node['effective_price_variability_penalty_score']:.4f}")
    
    # Show how adding resources changes top 5
    print("\n\nImpact of Resources on Rankings (Top 5 nodes with no resources vs. solar+battery):")
    print("-" * 100)
    
    results_none = all_results["none"]
    results_solar_battery = all_results["solar_battery"]
    
    print("\nNo On-Site Resources:")
    print(results_none.head(5)[['node', 'score_scenario', 'cost_score', 
                                  'price_variability_penalty_score']].to_string(index=False))
    
    print("\n\nWith Solar + Battery:")
    print(results_solar_battery.head(5)[['node', 'score_scenario', 'cost_score',
                                          'effective_price_variability_penalty_score']].to_string(index=False))
    
    return all_results


def demo_5_weight_comparison():
    """Example: Show how weights change across different load types."""
    print("\n" + "=" * 100)
    print("DEMO 5: Weight Analysis Across Load Types")
    print("=" * 100)
    print("Comparing how component weights differ for various load types\n")
    
    load_types = [
        "data_center_always_on",
        "data_center_flexible",
        "h2_electrolyzer_firm",
        "industrial_continuous",
        "industrial_flexible",
        "commercial_campus"
    ]
    
    # Common parameters
    load_size = 100  # MW
    emissions_pref = 50  # Moderate
    
    print(f"Parameters: Load Size = {load_size} MW, Emissions Preference = {emissions_pref}/100\n")
    print("-" * 100)
    print(f"{'Load Type':<30} {'Cost':<8} {'Land':<8} {'Policy':<8} {'Queue':<8} {'Emissions':<10} {'Variability':<12}")
    print("-" * 100)
    
    for load_type in load_types:
        weights = compute_final_weights(load_type, load_size, emissions_pref)
        print(f"{load_type:<30} {weights['cost']:.3f}    {weights['land']:.3f}    "
              f"{weights['policy']:.3f}    {weights['queue']:.3f}    "
              f"{weights['emissions']:.3f}      {weights['variability']:.3f}")
    
    print("\n\nKey Insights:")
    print("  - Data centers (always-on): High weight on land and variability")
    print("  - Data centers (flexible): Lower variability weight due to load flexibility")
    print("  - Electrolyzers: Very high emissions and queue weights, low land weight")
    print("  - Industrial: Balanced weights with emphasis on cost and queue")


def demo_6_emissions_sensitivity():
    """Example: Show impact of emissions preference slider."""
    print("\n" + "=" * 100)
    print("DEMO 6: Emissions Preference Sensitivity Analysis")
    print("=" * 100)
    print("How the emissions preference slider affects rankings\n")
    
    # Load data
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Common parameters
    common_params = {
        "nodes_df": nodes_df,
        "load_type": "data_center_always_on",
        "load_size_mw": 100,
        "location_filter": {"states": ["TX", "CA", "WA", "OR"]},
        "resource_config": "solar",
        "top_n": 5
    }
    
    # Test different emissions preferences
    emissions_prefs = [0, 25, 50, 75, 100]
    
    print("Testing emissions preferences: 0 (don't care) to 100 (very sensitive)\n")
    
    for pref in emissions_prefs:
        print(f"\n{'='*100}")
        print(f"Emissions Preference: {pref}/100")
        print('='*100)
        
        # Compute weights for this preference
        weights = compute_final_weights("data_center_always_on", 100, pref)
        print(f"Emissions Weight: {weights['emissions']:.3f} | Cost Weight: {weights['cost']:.3f}")
        
        # Run ranking
        results = rank_nodes(**common_params, emissions_preference=pref)
        
        print("\nTop 3 Nodes:")
        for idx, row in results.head(3).iterrows():
            print(f"  {row['rank_scenario']}. {row['node'][:30]:<30} {row['state']:<3} | "
                  f"Score: {row['score_scenario']:.3f} | "
                  f"Emissions: {row['county_emissions_intensity_kg_per_mwh']:>6.1f} kg/MWh | "
                  f"LMP: ${row['avg_lmp']:>6.2f}")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                     NODE RANKING ENGINE - DEMONSTRATIONS                      ║")
    print("║                                                                               ║")
    print("║  Fast, vectorized power system node ranking for large electric load siting   ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    
    try:
        # Run demonstrations
        demo_1_california_datacenter()
        demo_2_flexible_electrolyzer()
        demo_3_radial_search()
        demo_4_scenario_comparison()
        demo_5_weight_comparison()
        demo_6_emissions_sensitivity()
        
        print("\n" + "=" * 100)
        print("All demonstrations complete!")
        print("=" * 100)
        
    except Exception as e:
        print(f"\nError running demonstrations: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

