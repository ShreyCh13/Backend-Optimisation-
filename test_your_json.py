"""
Test Script for Your Exact JSON Format

Simply paste your JSON and run this script to see results.
"""

from api_wrapper import rank_nodes_from_frontend_json, format_response_for_frontend
import json


# ============================================================================
# PASTE YOUR JSON HERE
# ============================================================================

# Example 1: States mode
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

# Example 2: Points mode (uncomment to test)
# your_json = {
#     "loadConfig": {
#         "type": "industrial",
#         "subType": "continuous_process",
#         "sizeMW": 500,
#         "carbonEmissions": 30,
#         "onSiteGeneration": "yes",
#         "configurationType": "battery"
#     },
#     "location": {
#         "mode": "points",
#         "selectedStates": [],
#         "selectedPoints": [
#             {
#                 "id": "point-1763264891452",
#                 "lng": -108.72264303766178,
#                 "lat": 39.18291624575372
#             },
#             {
#                 "id": "point-1763264892236",
#                 "lng": -107.87709391027136,
#                 "lat": 41.76655632620444
#             },
#             {
#                 "id": "point-1763264892870",
#                 "lng": -106.16089408048168,
#                 "lat": 38.88393174385959
#             }
#         ]
#     }
# }


# ============================================================================
# RUN RANKING
# ============================================================================

def main():
    print("="*80)
    print("TESTING YOUR JSON INPUT")
    print("="*80)
    
    # Show input
    print("\nInput JSON:")
    print(json.dumps(your_json, indent=2))
    
    # Run ranking
    print("\n" + "="*80)
    print("RUNNING RANKING...")
    print("="*80)
    
    results = rank_nodes_from_frontend_json(your_json, top_n=10)
    
    # Display results in simple format
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    if len(results) == 0:
        print("\n❌ No results found!")
        return
    
    print(f"\n✅ Found {len(results)} results")
    print(f"\nTop 10 nodes:\n")
    print(f"{'Rank':<6} {'Node':<40} {'State':<6} {'Score':<8} {'LMP':<10}")
    print(f"{'-'*6} {'-'*40} {'-'*6} {'-'*8} {'-'*10}")
    
    for idx, row in results.head(10).iterrows():
        rank = int(row['rank_scenario'])
        node = str(row['node'])[:38]
        state = str(row['state'])
        score = row['score_scenario']
        lmp = row['avg_lmp']
        print(f"{rank:<6} {node:<40} {state:<6} {score:<8.4f} ${lmp:<9.2f}")
    
    # Show top node details
    top = results.iloc[0]
    print(f"\n{'='*80}")
    print("TOP NODE DETAILS")
    print(f"{'='*80}")
    print(f"\nNode: {top['node']}")
    print(f"Location: {top.get('county_state_pairs', top['state'])}")
    print(f"Coordinates: ({top['latitude']:.4f}, {top['longitude']:.4f})")
    print(f"ISO: {top.get('iso', 'N/A')}")
    print(f"\nOverall Score: {top['score_scenario']:.4f}")
    print(f"\nComponent Scores:")
    print(f"  Cost:        {top['cost_score']:.3f}  (lower energy cost is better)")
    print(f"  Land:        {top['land_score']:.3f}  (cheaper land is better)")
    print(f"  Emissions:   {top['emissions_score']:.3f}  (cleaner is better)")
    print(f"  Policy:      {top['policy_score']:.3f}  (more support is better)")
    print(f"  Queue:       {top['queue_score']:.3f}  (less congestion is better)")
    print(f"  Variability: {top['effective_price_variability_penalty_score']:.3f}  (more stable is better)")
    print(f"\nRaw Metrics:")
    print(f"  LMP:                ${top['avg_lmp']:.2f}/MWh")
    print(f"  Land Price:         ${top['avg_price_per_acre']:.0f}/acre")
    print(f"  Emissions:          {top['county_emissions_intensity_kg_per_mwh']:.1f} kg CO2/MWh")
    print(f"  Queue Pending:      {top.get('queue_pending_mw', 0):.0f} MW")
    
    # Format for frontend
    print(f"\n{'='*80}")
    print("FRONTEND-READY JSON OUTPUT (top 3)")
    print(f"{'='*80}\n")
    
    frontend_response = format_response_for_frontend(results.head(3))
    print(json.dumps(frontend_response, indent=2))
    
    # Export option
    print(f"\n{'='*80}")
    export_file = "results.csv"
    results.to_csv(export_file, index=False)
    print(f"✅ Full results exported to: {export_file}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()

