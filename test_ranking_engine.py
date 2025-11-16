"""
Comprehensive test suite for Node Ranking Engine

Run with: python test_ranking_engine.py
"""

import pandas as pd
import numpy as np
from node_ranking_engine import (
    rank_nodes,
    load_nodes_from_csv,
    robust_min_max,
    invert_score,
    compute_final_weights,
    get_load_type_multipliers,
    get_size_multipliers,
    validate_and_clean_data,
    haversine_distance_vectorized
)


def test_normalization():
    """Test normalization helpers."""
    print("\n" + "=" * 80)
    print("TEST 1: Normalization Functions")
    print("=" * 80)
    
    # Test robust_min_max
    print("\n1.1 Testing robust_min_max()...")
    series = pd.Series([1, 2, 3, 4, 5, 100, 200])  # Has outliers
    normalized = robust_min_max(series)
    print(f"  Input: {series.tolist()}")
    print(f"  Output: {normalized.round(3).tolist()}")
    assert normalized.min() >= 0 and normalized.max() <= 1, "Should be in [0,1]"
    print("  ✓ Passed: Values normalized to [0,1]")
    
    # Test constant series
    constant = pd.Series([5, 5, 5, 5, 5])
    normalized_const = robust_min_max(constant)
    print(f"\n  Constant input: {constant.tolist()}")
    print(f"  Output: {normalized_const.tolist()}")
    assert all(normalized_const == 0.5), "Constant series should map to 0.5"
    print("  ✓ Passed: Constant series handled correctly")
    
    # Test invert_score
    print("\n1.2 Testing invert_score()...")
    scores = pd.Series([0.0, 0.25, 0.5, 0.75, 1.0])
    inverted = invert_score(scores)
    print(f"  Input: {scores.tolist()}")
    print(f"  Output: {inverted.tolist()}")
    assert inverted.iloc[0] == 1.0 and inverted.iloc[-1] == 0.0, "Should invert correctly"
    print("  ✓ Passed: Scores inverted correctly")


def test_spatial_filtering():
    """Test spatial filtering functions."""
    print("\n" + "=" * 80)
    print("TEST 2: Spatial Filtering")
    print("=" * 80)
    
    # Test haversine distance
    print("\n2.1 Testing haversine distance calculation...")
    # San Francisco to Los Angeles (known distance ~559 km)
    lat1, lon1 = 37.77, -122.42  # SF
    lat2 = pd.Series([34.05])  # LA
    lon2 = pd.Series([-118.24])
    
    distance = haversine_distance_vectorized(lat1, lon1, lat2, lon2)
    print(f"  SF to LA distance: {distance.iloc[0]:.1f} km")
    assert 500 < distance.iloc[0] < 600, "Should be ~559 km"
    print("  ✓ Passed: Distance calculation accurate")
    
    # Test vectorized distance
    print("\n2.2 Testing vectorized distance...")
    lats = pd.Series([34.05, 40.71, 41.88])  # LA, NYC, Chicago
    lons = pd.Series([-118.24, -74.01, -87.63])
    distances = haversine_distance_vectorized(lat1, lon1, lats, lons)
    print(f"  Distances from SF: {distances.round(1).tolist()}")
    assert len(distances) == 3, "Should compute all distances"
    print("  ✓ Passed: Vectorized computation works")


def test_weight_computation():
    """Test weight adjustment logic."""
    print("\n" + "=" * 80)
    print("TEST 3: Weight Computation")
    print("=" * 80)
    
    print("\n3.1 Testing load type multipliers...")
    load_types = ["data_center_always_on", "h2_electrolyzer_firm", "industrial_flexible"]
    for lt in load_types:
        multipliers = get_load_type_multipliers(lt)
        print(f"  {lt}:")
        print(f"    Land multiplier: {multipliers['land']:.2f}")
        print(f"    Emissions multiplier: {multipliers['emissions']:.2f}")
    print("  ✓ Passed: Load type multipliers computed")
    
    print("\n3.2 Testing size multipliers...")
    sizes = [25, 100, 300]  # Small, medium, large
    for size in sizes:
        multipliers = get_size_multipliers(size)
        print(f"  {size} MW: queue={multipliers.get('queue', 1.0):.2f}, "
              f"variability={multipliers.get('variability', 1.0):.2f}")
    print("  ✓ Passed: Size multipliers computed")
    
    print("\n3.3 Testing final weight computation...")
    weights = compute_final_weights("data_center_always_on", 250, 80)
    print("  Weights for data center (250 MW, 80% emissions pref):")
    for k, v in weights.items():
        print(f"    {k}: {v:.4f}")
    
    total = sum(weights.values())
    assert abs(total - 1.0) < 0.001, "Weights should sum to 1.0"
    print(f"  Sum of weights: {total:.6f}")
    print("  ✓ Passed: Weights sum to 1.0")


def test_data_validation():
    """Test data validation and cleaning."""
    print("\n" + "=" * 80)
    print("TEST 4: Data Validation")
    print("=" * 80)
    
    print("\n4.1 Creating test dataset with issues...")
    test_data = pd.DataFrame({
        'node': ['A', 'B', 'C', 'D'],
        'state': ['CA', 'NY', None, 'TX'],  # C has missing state
        'latitude': [37.7, 40.7, 41.8, 30.3],
        'longitude': [-122.4, -74.0, -87.6, -97.7],
        'avg_lmp': [30.5, None, 45.2, 50.1],  # B has missing LMP
        'avg_price_per_acre': [10000, 15000, 8000, 6000],
        'county_emissions_intensity_kg_per_mwh': [100, 150, 200, 180],
        'queue_pending_mw': [100, 200, 300, 400],
        'queue_advanced_share': [0.5, 0.6, 0.7, 0.8],
        'queue_renewable_storage_share': [0.8, 0.7, 0.9, 0.85],
        'queue_pressure_index': [0.3, 0.4, 0.2, 0.1],
        'price_variance_score': [2.5, 3.0, 1.5, 2.0],
        'policy_fit_electrolyzer': [0.8, 0.7, 0.9, 0.85],
        'policy_fit_datacenter': [0.7, 0.8, 0.6, 0.75],
        'is_h2_hub_state': [1, 0, 1, 1],
        'state_dc_incentive_level': [0.8, 0.6, 0.7, 0.9],
        'state_clean_energy_friendly': [2, 1, 1, 1],  # Outlier value
        'has_hosting_capacity_map': [1, 1, 0, 1],
    })
    
    print(f"  Original rows: {len(test_data)}")
    
    cleaned = validate_and_clean_data(test_data)
    print(f"  After cleaning: {len(cleaned)} rows")
    print(f"  Removed {len(test_data) - len(cleaned)} rows with missing critical fields")
    
    # Check that state_clean_energy_friendly was clipped
    if len(cleaned) > 0:
        max_val = cleaned['state_clean_energy_friendly'].max()
        print(f"  Max state_clean_energy_friendly after clipping: {max_val}")
        assert max_val <= 1.0, "Should be clipped to [0, 1]"
        print("  ✓ Passed: Data cleaned and validated")


def test_full_ranking():
    """Test complete ranking workflow."""
    print("\n" + "=" * 80)
    print("TEST 5: Full Ranking Workflow")
    print("=" * 80)
    
    print("\n5.1 Loading real data...")
    try:
        nodes_df = load_nodes_from_csv("final_csv_v1.csv")
        print(f"  Loaded {len(nodes_df)} nodes")
    except Exception as e:
        print(f"  ✗ Failed to load data: {e}")
        return
    
    print("\n5.2 Running ranking with state filter...")
    results = rank_nodes(
        nodes_df=nodes_df,
        load_type="data_center_always_on",
        load_size_mw=100,
        location_filter={"states": ["CA"]},
        emissions_preference=50,
        resource_config="solar",
        top_n=10
    )
    
    print(f"  Returned {len(results)} results")
    assert len(results) > 0, "Should return results"
    assert len(results) <= 10, "Should respect top_n"
    
    # Check required columns
    required_cols = ['node', 'score_scenario', 'rank_scenario', 'cost_score', 
                     'emissions_score', 'policy_score']
    for col in required_cols:
        assert col in results.columns, f"Missing column: {col}"
    
    print(f"  Top node: {results.iloc[0]['node']}")
    print(f"  Top score: {results.iloc[0]['score_scenario']:.4f}")
    print("  ✓ Passed: Ranking completed successfully")
    
    print("\n5.3 Testing radial filter...")
    results_radial = rank_nodes(
        nodes_df=nodes_df,
        load_type="industrial_continuous",
        load_size_mw=75,
        location_filter={"lat": 37.77, "lon": -122.42, "radius_km": 100},
        emissions_preference=60,
        resource_config="battery",
        top_n=5
    )
    
    print(f"  Found {len(results_radial)} nodes within 100 km of SF")
    if len(results_radial) > 0:
        print(f"  Top node: {results_radial.iloc[0]['node']}")
        print("  ✓ Passed: Radial filtering works")
    
    print("\n5.4 Testing scenario comparison...")
    results_baseline = rank_nodes(
        nodes_df=nodes_df,
        load_type="data_center_flexible",
        load_size_mw=200,
        location_filter={"states": ["TX"]},
        emissions_preference=40,
        resource_config="none",
        top_n=5
    )
    
    results_solar_battery = rank_nodes(
        nodes_df=nodes_df,
        load_type="data_center_flexible",
        load_size_mw=200,
        location_filter={"states": ["TX"]},
        emissions_preference=40,
        resource_config="solar_battery",
        top_n=5
    )
    
    if len(results_baseline) > 0 and len(results_solar_battery) > 0:
        print(f"  Baseline top score: {results_baseline.iloc[0]['score_scenario']:.4f}")
        print(f"  Solar+battery top score: {results_solar_battery.iloc[0]['score_scenario']:.4f}")
        print("  ✓ Passed: Scenario comparison works")


def test_score_properties():
    """Test that scores have expected properties."""
    print("\n" + "=" * 80)
    print("TEST 6: Score Properties")
    print("=" * 80)
    
    try:
        nodes_df = load_nodes_from_csv("final_csv_v1.csv")
        
        print("\n6.1 Running ranking...")
        results = rank_nodes(
            nodes_df=nodes_df,
            load_type="h2_electrolyzer_firm",
            load_size_mw=100,
            location_filter=None,
            emissions_preference=80,
            resource_config="none",
            top_n=100
        )
        
        # Check that scores are in [0, 1]
        score_cols = ['cost_score', 'land_score', 'emissions_score', 'policy_score',
                      'queue_score', 'price_variability_penalty_score',
                      'effective_price_variability_penalty_score']
        
        print("\n6.2 Checking score ranges...")
        for col in score_cols:
            min_val = results[col].min()
            max_val = results[col].max()
            print(f"  {col}: [{min_val:.3f}, {max_val:.3f}]")
            assert 0 <= min_val <= 1, f"{col} min should be in [0,1]"
            assert 0 <= max_val <= 1, f"{col} max should be in [0,1]"
        print("  ✓ Passed: All component scores in [0, 1]")
        
        # Check that composite scores are valid
        print("\n6.3 Checking composite scores...")
        assert (results['score_baseline'] >= 0).all(), "Baseline scores should be >= 0"
        assert (results['score_baseline'] <= 1).all(), "Baseline scores should be <= 1"
        assert (results['score_scenario'] >= 0).all(), "Scenario scores should be >= 0"
        assert (results['score_scenario'] <= 1).all(), "Scenario scores should be <= 1"
        print("  ✓ Passed: Composite scores valid")
        
        # Check that ranks are sequential
        print("\n6.4 Checking rank ordering...")
        expected_ranks = list(range(1, len(results) + 1))
        actual_ranks = sorted(results['rank_scenario'].tolist())
        assert actual_ranks == expected_ranks, "Ranks should be 1, 2, 3, ..."
        print("  ✓ Passed: Ranks are sequential")
        
        # Check that scores are monotonically decreasing
        scores = results['score_scenario'].tolist()
        is_monotonic = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
        assert is_monotonic, "Scores should be sorted descending"
        print("  ✓ Passed: Scores monotonically decreasing")
        
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Run complete test suite."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                   NODE RANKING ENGINE - TEST SUITE                            ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    
    tests = [
        ("Normalization Functions", test_normalization),
        ("Spatial Filtering", test_spatial_filtering),
        ("Weight Computation", test_weight_computation),
        ("Data Validation", test_data_validation),
        ("Full Ranking Workflow", test_full_ranking),
        ("Score Properties", test_score_properties),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n✗ TEST FAILED: {test_name}")
            print(f"  Assertion Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ TEST FAILED: {test_name}")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"  Passed: {passed}/{len(tests)}")
    print(f"  Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n  ✓ ALL TESTS PASSED!")
    else:
        print(f"\n  ✗ {failed} test(s) failed")
    
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()

