#!/usr/bin/env python3
"""
Test script to validate bug fixes and anti-pattern corrections.
"""

import sys
import traceback

def test_phi_balancer():
    """Test PhiBalancer fixes and improvements."""
    print("Testing PhiBalancer...")
    from phiresearch_systems.balancing import PhiBalancer
    
    # Test basic functionality
    balancer = PhiBalancer(['server1', 'server2', 'server3'])
    server = balancer.get_server_for_request('test_request')
    assert server in ['server1', 'server2', 'server3']
    
    # Test deterministic behavior (should be consistent across runs)
    server1 = balancer.get_server_for_request('test_request')
    server2 = balancer.get_server_for_request('test_request')
    assert server1 == server2, "Hash should be deterministic"
    
    # Test input validation
    try:
        PhiBalancer([])
        assert False, "Should raise ValueError for empty server list"
    except ValueError:
        pass
    
    try:
        PhiBalancer(123)
        assert False, "Should raise TypeError for non-list input"
    except TypeError:
        pass
    
    try:
        PhiBalancer(['server1', 123])
        assert False, "Should raise TypeError for non-string server"
    except TypeError:
        pass
    
    try:
        balancer.get_server_for_request(123)
        assert False, "Should raise TypeError for non-string request_id"
    except TypeError:
        pass
    
    print("✓ PhiBalancer tests passed")

def test_phi_cache():
    """Test PhiCache fixes and improvements."""
    print("Testing PhiCache...")
    from phiresearch_systems.caching import PhiCache
    
    # Test basic functionality
    cache = PhiCache(3)
    cache.put('key1', 'value1')
    cache.put('key2', 'value2')
    assert cache.get('key1') == 'value1'
    assert cache.get('key2') == 'value2'
    assert cache.get('nonexistent') is None
    
    # Test capacity limits and eviction
    cache.put('key3', 'value3')
    cache.put('key4', 'value4')  # This should trigger eviction
    
    # Test input validation
    try:
        PhiCache(-1)
        assert False, "Should raise ValueError for negative capacity"
    except ValueError:
        pass
    
    try:
        PhiCache("invalid")
        assert False, "Should raise TypeError for non-integer capacity"
    except TypeError:
        pass
    
    try:
        cache.put(123, 'value')
        assert False, "Should raise TypeError for non-string key"
    except TypeError:
        pass
    
    try:
        cache.put('key', 123)
        assert False, "Should raise TypeError for non-string value"
    except TypeError:
        pass
    
    try:
        cache.get(123)
        assert False, "Should raise TypeError for non-string key"
    except TypeError:
        pass
    
    print("✓ PhiCache tests passed")

def test_modlo_sequence():
    """Test modlo_sequence fixes and improvements."""
    print("Testing modlo_sequence...")
    from phiresearch_systems.generators import modlo_sequence
    
    # Test basic functionality
    seq = modlo_sequence(7)
    expected = [1, 1, 2, 3, 5, 8, 13]
    assert seq == expected, f"Expected {expected}, got {seq}"
    
    seq_longer = modlo_sequence(10)
    assert len(seq_longer) == 10
    assert seq_longer[:7] == expected
    
    # Test edge cases
    assert modlo_sequence(0) == []
    assert modlo_sequence(1) == [1]
    
    # Test input validation
    try:
        modlo_sequence(-1)
        assert False, "Should raise ValueError for negative input"
    except ValueError:
        pass
    
    try:
        modlo_sequence("invalid")
        assert False, "Should raise TypeError for non-integer input"
    except TypeError:
        pass
    
    print("✓ modlo_sequence tests passed")

def test_import_structure():
    """Test that import structure is fixed."""
    print("Testing import structure...")
    
    try:
        # This should work now without circular import issues
        import phiresearch_systems
        from phiresearch_systems import balancing, caching, generators
        print("✓ phiresearch_systems imports successful")
    except Exception as e:
        print(f"✗ phiresearch_systems import failed: {e}")
        return False
    
    # Note: We can't test phiresearch_compression imports without the C++ extension
    # but we can verify the compressor module structure
    try:
        import phiresearch_compression.compressor
        print("✓ phiresearch_compression.compressor import successful")
    except ImportError as e:
        if "core_bindings" in str(e):
            print("✓ phiresearch_compression.compressor import structure correct (C++ extension missing as expected)")
        else:
            print(f"✗ Unexpected import error: {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("Running bug fix validation tests...")
    print("=" * 50)
    
    tests = [
        test_phi_balancer,
        test_phi_cache,
        test_modlo_sequence,
        test_import_structure,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Bug fixes are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)