"""
Interactive Test Interface for Node Ranking Engine

A simple command-line interface for testing different input combinations.
Run with: python interactive_test.py
"""

from node_ranking_engine import rank_nodes, load_nodes_from_csv, compute_final_weights
import pandas as pd


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")


def print_section(text):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'-'*len(text)}{Colors.END}")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")


def get_choice(prompt, options, default=None):
    """Get a choice from user with validation."""
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")
    for i, (key, desc) in enumerate(options.items(), 1):
        default_marker = f" {Colors.GREEN}(default){Colors.END}" if key == default else ""
        print(f"  {i}. {key:<30} - {desc}{default_marker}")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Enter choice (1-{len(options)}) or press Enter for default: {Colors.END}").strip()
        
        if not choice and default:
            return default
        
        try:
            idx = int(choice)
            if 1 <= idx <= len(options):
                return list(options.keys())[idx - 1]
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")


def get_number(prompt, min_val=None, max_val=None, default=None):
    """Get a number from user with validation."""
    default_text = f" (default: {default})" if default is not None else ""
    range_text = ""
    if min_val is not None and max_val is not None:
        range_text = f" [{min_val}-{max_val}]"
    elif min_val is not None:
        range_text = f" [>={min_val}]"
    elif max_val is not None:
        range_text = f" [<={max_val}]"
    
    while True:
        value = input(f"\n{Colors.BOLD}{prompt}{range_text}{default_text}: {Colors.END}").strip()
        
        if not value and default is not None:
            return default
        
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                print_error(f"Value must be >= {min_val}")
                continue
            if max_val is not None and num > max_val:
                print_error(f"Value must be <= {max_val}")
                continue
            return num
        except ValueError:
            print_error("Please enter a valid number")


def get_states():
    """Get state filter from user."""
    print(f"\n{Colors.BOLD}Enter states (comma-separated, e.g., CA,NY,TX) or press Enter for no filter:{Colors.END}")
    states_input = input(f"{Colors.BOLD}States: {Colors.END}").strip()
    
    if not states_input:
        return None
    
    states = [s.strip().upper() for s in states_input.split(',')]
    return {"states": states}


def get_radial_filter():
    """Get radial filter from user."""
    print(f"\n{Colors.BOLD}Enter radial search parameters:{Colors.END}")
    
    lat = get_number("Latitude", min_val=-90, max_val=90)
    lon = get_number("Longitude", min_val=-180, max_val=180)
    radius = get_number("Radius (km)", min_val=1, max_val=5000)
    
    return {"lat": lat, "lon": lon, "radius_km": radius}


def get_location_filter():
    """Get location filter from user."""
    options = {
        "none": "No spatial filter (search all locations)",
        "states": "Filter by state(s)",
        "radial": "Radial search around a point"
    }
    
    choice = get_choice("Select location filter:", options, default="none")
    
    if choice == "none":
        return None
    elif choice == "states":
        return get_states()
    else:
        return get_radial_filter()


def display_results(results, show_full=False):
    """Display ranking results in a formatted way."""
    if len(results) == 0:
        print_error("No results returned!")
        return
    
    print_section("RANKING RESULTS")
    
    # Summary
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Total results: {len(results)}")
    print(f"  Top node: {results.iloc[0]['node']}")
    print(f"  Top score: {results.iloc[0]['score_scenario']:.4f}")
    
    # Top 10 results
    num_to_show = min(10, len(results))
    print(f"\n{Colors.BOLD}Top {num_to_show} Nodes:{Colors.END}\n")
    
    # Header
    print(f"{'Rank':<6} {'Node':<35} {'State':<6} {'ISO':<15} {'Score':<8} {'LMP':<10}")
    print(f"{'-'*6} {'-'*35} {'-'*6} {'-'*15} {'-'*8} {'-'*10}")
    
    # Rows
    for idx, row in results.head(num_to_show).iterrows():
        rank = f"{int(row['rank_scenario'])}"
        node = row['node'][:33] if len(str(row['node'])) > 33 else str(row['node'])
        state = str(row['state'])
        iso = str(row['iso'])[:13] if len(str(row['iso'])) > 13 else str(row['iso'])
        score = f"{row['score_scenario']:.4f}"
        lmp = f"${row['avg_lmp']:.2f}"
        
        print(f"{rank:<6} {node:<35} {state:<6} {iso:<15} {score:<8} {lmp:<10}")
    
    # Component scores for top node
    if show_full:
        print(f"\n{Colors.BOLD}Component Scores (Top Node):{Colors.END}")
        top = results.iloc[0]
        print(f"  Cost Score:       {top['cost_score']:.3f}")
        print(f"  Land Score:       {top['land_score']:.3f}")
        print(f"  Emissions Score:  {top['emissions_score']:.3f}")
        print(f"  Policy Score:     {top['policy_score']:.3f}")
        print(f"  Queue Score:      {top['queue_score']:.3f}")
        print(f"  Variability:      {top['effective_price_variability_penalty_score']:.3f}")
        
        # Geographic distribution
        print(f"\n{Colors.BOLD}Geographic Distribution:{Colors.END}")
        state_counts = results['state'].value_counts().head(5)
        for state, count in state_counts.items():
            pct = (count / len(results)) * 100
            print(f"  {state}: {count} nodes ({pct:.1f}%)")
    
    # Export option
    print(f"\n{Colors.BOLD}Export results?{Colors.END}")
    export = input("Enter filename to export (or press Enter to skip): ").strip()
    if export:
        if not export.endswith('.csv'):
            export += '.csv'
        results.to_csv(export, index=False)
        print_success(f"Results exported to {export}")


def run_ranking_test(nodes_df):
    """Run a single ranking test with user inputs."""
    print_header("CONFIGURE RANKING PARAMETERS")
    
    # 1. Load Type
    load_types = {
        "data_center_always_on": "Constant load data center (24/7)",
        "data_center_flexible": "Flexible/interruptible data center",
        "h2_electrolyzer_firm": "Hydrogen electrolyzer (firm load)",
        "industrial_continuous": "Continuous industrial process (24/7)",
        "industrial_flexible": "Flexible industrial load",
        "commercial_campus": "Commercial/office campus"
    }
    load_type = get_choice("Select load type:", load_types, default="data_center_always_on")
    
    # 2. Load Size
    load_size_mw = get_number("Enter load size (MW)", min_val=1, max_val=10000, default=100)
    
    # 3. Location Filter
    location_filter = get_location_filter()
    
    # 4. Emissions Preference
    print_info("Emissions preference: 0 = don't care, 100 = extremely sensitive")
    emissions_preference = get_number("Enter emissions preference", min_val=0, max_val=100, default=50)
    
    # 5. Resource Configuration
    resource_configs = {
        "none": "Grid-only (no on-site resources)",
        "solar": "On-site solar generation",
        "battery": "On-site battery storage",
        "solar_battery": "Solar + battery combination",
        "firm_gen": "Firm on-site generation (gas, etc.)"
    }
    resource_config = get_choice("Select resource configuration:", resource_configs, default="none")
    
    # 6. Top N
    top_n = int(get_number("Number of top results to return", min_val=1, max_val=1000, default=10))
    
    # Show weight breakdown
    print_section("WEIGHT BREAKDOWN")
    weights = compute_final_weights(load_type, load_size_mw, emissions_preference)
    print("\nComponent weights for your configuration:")
    for component, weight in weights.items():
        bar = '█' * int(weight * 50)
        print(f"  {component:12} {weight:.4f} {bar}")
    
    # Confirmation
    print_section("CONFIGURATION SUMMARY")
    print(f"  Load Type:            {load_type}")
    print(f"  Load Size:            {load_size_mw} MW")
    print(f"  Location Filter:      {location_filter if location_filter else 'None (all locations)'}")
    print(f"  Emissions Pref:       {emissions_preference}/100")
    print(f"  Resource Config:      {resource_config}")
    print(f"  Top N:                {top_n}")
    
    print(f"\n{Colors.BOLD}Run ranking with these parameters? (y/n): {Colors.END}", end='')
    if input().strip().lower() != 'y':
        print_info("Ranking cancelled")
        return
    
    # Run ranking
    print_header("RUNNING RANKING...")
    
    try:
        results = rank_nodes(
            nodes_df=nodes_df,
            load_type=load_type,
            load_size_mw=load_size_mw,
            location_filter=location_filter,
            emissions_preference=emissions_preference,
            resource_config=resource_config,
            top_n=top_n
        )
        
        print_success("Ranking completed successfully!")
        display_results(results, show_full=True)
        
    except Exception as e:
        print_error(f"Error during ranking: {e}")
        import traceback
        traceback.print_exc()


def quick_scenarios(nodes_df):
    """Run predefined quick scenarios for comparison."""
    print_header("QUICK SCENARIO TESTS")
    
    scenarios = {
        "1": {
            "name": "CA Data Center (250 MW, high emissions sensitivity)",
            "params": {
                "load_type": "data_center_always_on",
                "load_size_mw": 250,
                "location_filter": {"states": ["CA"]},
                "emissions_preference": 80,
                "resource_config": "solar_battery",
                "top_n": 5
            }
        },
        "2": {
            "name": "National H2 Electrolyzer (100 MW)",
            "params": {
                "load_type": "h2_electrolyzer_firm",
                "load_size_mw": 100,
                "location_filter": None,
                "emissions_preference": 90,
                "resource_config": "none",
                "top_n": 5
            }
        },
        "3": {
            "name": "TX Industrial (75 MW, cost-focused)",
            "params": {
                "load_type": "industrial_continuous",
                "load_size_mw": 75,
                "location_filter": {"states": ["TX"]},
                "emissions_preference": 30,
                "resource_config": "battery",
                "top_n": 5
            }
        },
        "4": {
            "name": "Multi-state flexible data center comparison",
            "params": {
                "load_type": "data_center_flexible",
                "load_size_mw": 150,
                "location_filter": {"states": ["CA", "TX", "NY", "WA"]},
                "emissions_preference": 60,
                "resource_config": "solar",
                "top_n": 10
            }
        }
    }
    
    print("Select a quick scenario to run:\n")
    for key, scenario in scenarios.items():
        print(f"  {key}. {scenario['name']}")
    print(f"  5. Run all scenarios")
    
    choice = input(f"\n{Colors.BOLD}Enter choice (1-5): {Colors.END}").strip()
    
    if choice == "5":
        # Run all scenarios
        for key, scenario in scenarios.items():
            print_header(f"SCENARIO {key}: {scenario['name']}")
            try:
                results = rank_nodes(nodes_df=nodes_df, **scenario['params'])
                print_success(f"Completed: {len(results)} results")
                display_results(results, show_full=False)
            except Exception as e:
                print_error(f"Error: {e}")
    elif choice in scenarios:
        scenario = scenarios[choice]
        print_header(f"SCENARIO: {scenario['name']}")
        try:
            results = rank_nodes(nodes_df=nodes_df, **scenario['params'])
            print_success(f"Completed: {len(results)} results")
            display_results(results, show_full=True)
        except Exception as e:
            print_error(f"Error: {e}")
    else:
        print_error("Invalid choice")


def main():
    """Main interactive loop."""
    print_header("NODE RANKING ENGINE - INTERACTIVE TEST INTERFACE")
    
    # Load data
    print_section("Loading Data")
    try:
        nodes_df = load_nodes_from_csv("final_csv_v1.csv")
        print_success(f"Loaded {len(nodes_df):,} nodes from final_csv_v1.csv")
    except Exception as e:
        print_error(f"Failed to load data: {e}")
        return
    
    # Main loop
    while True:
        print_section("MAIN MENU")
        print("\n1. Custom ranking test (configure all parameters)")
        print("2. Quick scenario tests (predefined scenarios)")
        print("3. Exit")
        
        choice = input(f"\n{Colors.BOLD}Enter choice (1-3): {Colors.END}").strip()
        
        if choice == "1":
            run_ranking_test(nodes_df)
        elif choice == "2":
            quick_scenarios(nodes_df)
        elif choice == "3":
            print_success("\nThank you for using the Node Ranking Engine!")
            print_header("GOODBYE")
            break
        else:
            print_error("Invalid choice. Please enter 1, 2, or 3.")
        
        # Ask to continue
        if choice in ["1", "2"]:
            print(f"\n{Colors.BOLD}Run another test? (y/n): {Colors.END}", end='')
            if input().strip().lower() != 'y':
                print_success("\nThank you for using the Node Ranking Engine!")
                print_header("GOODBYE")
                break


if __name__ == "__main__":
    main()

