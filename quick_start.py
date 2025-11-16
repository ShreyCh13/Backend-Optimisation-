"""
Quick Start Guide for Node Ranking Engine

This script provides simple, copy-paste examples to get started quickly.
"""

from node_ranking_engine import rank_nodes, load_nodes_from_csv


def example_1_simple():
    """Simplest possible example - just rank nodes."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simplest Usage")
    print("="*80)
    
    # Load data
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Rank nodes
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="data_center_always_on",
        load_size_mw=100,
        location_filter=None,  # No spatial filter
        emissions_preference=50,
        resource_config="none",
        top_n=10
    )
    
    # Display results
    print("\nTop 10 nodes:")
    print(results[['node', 'state', 'score_scenario', 'rank_scenario']].to_string(index=False))


def example_2_state_filter():
    """Example with state filtering."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Filter by States")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Rank nodes in specific states
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="data_center_flexible",
        load_size_mw=200,
        location_filter={"states": ["CA", "OR", "WA"]},  # West Coast only
        emissions_preference=75,  # High emissions sensitivity
        resource_config="solar_battery",
        top_n=5
    )
    
    print("\nTop 5 nodes in CA/OR/WA:")
    for idx, row in results.iterrows():
        print(f"\n{row['rank_scenario']}. {row['node']} ({row['state']})")
        print(f"   Score: {row['score_scenario']:.3f}")
        print(f"   LMP: ${row['avg_lmp']:.2f}/MWh")
        print(f"   Emissions: {row['county_emissions_intensity_kg_per_mwh']:.0f} kg/MWh")


def example_3_radial_search():
    """Example with radial search around a point."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Radial Search")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Find nodes within 150 km of Houston, TX (29.76, -95.37)
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="industrial_continuous",
        load_size_mw=50,
        location_filter={"lat": 29.76, "lon": -95.37, "radius_km": 150},
        emissions_preference=30,
        resource_config="battery",
        top_n=10
    )
    
    print(f"\nFound {len(results)} nodes within 150 km of Houston")
    print("\nTop 5:")
    print(results.head(5)[['node', 'county_state_pairs', 'score_scenario']].to_string(index=False))


def example_4_compare_scenarios():
    """Compare different resource configurations."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Compare Resource Scenarios")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    # Common parameters
    params = {
        "nodes_df": nodes_df,
        "load_type": "data_center_always_on",
        "load_size_mw": 300,
        "location_filter": {"states": ["TX"]},
        "emissions_preference": 60,
        "top_n": 3
    }
    
    scenarios = {
        "Grid Only": "none",
        "With Solar": "solar",
        "With Battery": "battery",
        "Solar + Battery": "solar_battery",
        "Firm Gen": "firm_gen"
    }
    
    print("\nComparing resource configurations for 300 MW data center in Texas:\n")
    print(f"{'Scenario':<20} {'Top Node':<30} {'Score':<8}")
    print("-" * 60)
    
    for scenario_name, resource_config in scenarios.items():
        results = rank_nodes(**params, resource_config=resource_config)
        if len(results) > 0:
            top = results.iloc[0]
            print(f"{scenario_name:<20} {top['node'][:28]:<30} {top['score_scenario']:.4f}")


def example_5_different_loads():
    """Compare rankings for different load types."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Different Load Types")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    load_types = {
        "Always-On Data Center": "data_center_always_on",
        "Flexible Data Center": "data_center_flexible",
        "H2 Electrolyzer": "h2_electrolyzer_firm",
        "Industrial": "industrial_continuous"
    }
    
    print("\nTop node for each load type (national search):\n")
    print(f"{'Load Type':<25} {'Top Node':<30} {'State':<5} {'Score':<8}")
    print("-" * 70)
    
    for load_name, load_type in load_types.items():
        results = rank_nodes(
            nodes_df=nodes_df,
            load_type=load_type,
            load_size_mw=100,
            location_filter=None,
            emissions_preference=50,
            resource_config="none",
            top_n=1
        )
        if len(results) > 0:
            top = results.iloc[0]
            print(f"{load_name:<25} {top['node'][:28]:<30} {top['state']:<5} {top['score_scenario']:.4f}")


def example_6_emissions_sensitivity():
    """Show impact of emissions preference."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Emissions Sensitivity")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    print("\nHow top node changes with emissions preference:\n")
    print(f"{'Preference':<15} {'Top Node':<30} {'State':<5} {'Emissions (kg/MWh)':<20}")
    print("-" * 75)
    
    for emissions_pref in [0, 25, 50, 75, 100]:
        results = rank_nodes(
            nodes_df=nodes_df,
            load_type="data_center_always_on",
            load_size_mw=150,
            location_filter={"states": ["CA", "TX", "NY"]},
            emissions_preference=emissions_pref,
            resource_config="solar",
            top_n=1
        )
        if len(results) > 0:
            top = results.iloc[0]
            emissions = top['county_emissions_intensity_kg_per_mwh']
            print(f"{emissions_pref:<15} {top['node'][:28]:<30} {top['state']:<5} {emissions:>18.1f}")


def example_7_export_results():
    """Save results to CSV."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Export Results to CSV")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="h2_electrolyzer_firm",
        load_size_mw=100,
        location_filter=None,
        emissions_preference=90,
        resource_config="none",
        top_n=50
    )
    
    # Save to CSV
    output_file = "ranking_results_h2_electrolyzer_top50.csv"
    results.to_csv(output_file, index=False)
    print(f"\nSaved {len(results)} results to {output_file}")
    
    # Show what columns are available
    print("\nAvailable columns:")
    for col in results.columns:
        print(f"  - {col}")


def example_8_custom_analysis():
    """Perform custom analysis on results."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Custom Analysis")
    print("="*80)
    
    nodes_df = load_nodes_from_csv("final_csv_v1.csv")
    
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="industrial_flexible",
        load_size_mw=75,
        location_filter={"states": ["CA", "TX", "NY", "IL", "PA"]},
        emissions_preference=60,
        resource_config="battery",
        top_n=100
    )
    
    print("\nCustom Analysis on Top 100 Results:")
    print("-" * 80)
    
    # Average metrics
    print(f"\nAverage LMP: ${results['avg_lmp'].mean():.2f}/MWh")
    print(f"Average Emissions: {results['county_emissions_intensity_kg_per_mwh'].mean():.1f} kg/MWh")
    print(f"Average Land Price: ${results['avg_price_per_acre'].mean():.0f}/acre")
    
    # Distribution by state
    print("\nDistribution by State:")
    state_counts = results['state'].value_counts()
    for state, count in state_counts.items():
        pct = (count / len(results)) * 100
        print(f"  {state}: {count} nodes ({pct:.1f}%)")
    
    # Distribution by ISO
    print("\nDistribution by ISO:")
    iso_counts = results['iso'].value_counts()
    for iso, count in iso_counts.items():
        pct = (count / len(results)) * 100
        print(f"  {iso}: {count} nodes ({pct:.1f}%)")
    
    # Top 5 by specific components
    print("\nTop 5 by Cost Score:")
    top_cost = results.nlargest(5, 'cost_score')
    for idx, row in top_cost.iterrows():
        print(f"  {row['node']}: {row['cost_score']:.3f} (LMP: ${row['avg_lmp']:.2f})")
    
    print("\nTop 5 by Emissions Score:")
    top_emissions = results.nlargest(5, 'emissions_score')
    for idx, row in top_emissions.iterrows():
        emissions = row['county_emissions_intensity_kg_per_mwh']
        print(f"  {row['node']}: {row['emissions_score']:.3f} ({emissions:.1f} kg/MWh)")


def main():
    """Run all examples."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                   NODE RANKING ENGINE - QUICK START                           ║")
    print("║                                                                               ║")
    print("║  Copy and adapt these examples to get started quickly                        ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    
    # Run examples (comment out any you don't want to run)
    example_1_simple()
    example_2_state_filter()
    example_3_radial_search()
    example_4_compare_scenarios()
    example_5_different_loads()
    example_6_emissions_sensitivity()
    example_7_export_results()
    example_8_custom_analysis()
    
    print("\n" + "="*80)
    print("Quick start examples complete!")
    print("="*80)
    print("\nNext steps:")
    print("  1. Modify these examples for your use case")
    print("  2. See demo_ranking.py for more complex scenarios")
    print("  3. See README.md for complete API documentation")
    print("  4. Run test_ranking_engine.py to validate your setup")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

