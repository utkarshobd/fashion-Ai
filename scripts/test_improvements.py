"""
Integration Test Script

Verifies that all improvements are working correctly:
1. Logging is properly set up
2. Configuration is loaded correctly
3. Input validation works
4. Error handling doesn't crash the system
5. LLM response validation catches invalid responses

Run this after making improvements to ensure nothing is broken.

Usage:
    python test_improvements.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from conversational_multimodal_fashion_intelligence_system.logger import get_logger, setup_logging
from conversational_multimodal_fashion_intelligence_system.config import config
from conversational_multimodal_fashion_intelligence_system.validators import InputValidator, safe_validate
from recommendation_architecture.text_parser import parse_text_input
from recommendation_architecture.confidence_handler import (
    is_low_confidence, confidence_label, explain_confidence
)
from recommendation_architecture.rule_engine import validate_prediction

# Setup logging for tests
logger = get_logger(__name__)

print("=" * 60)
print("FASHION AI - IMPROVEMENT VERIFICATION TESTS")
print("=" * 60)

# ============== TEST 1: LOGGING ==============
print("\n[TEST 1] Logging Framework")
print("-" * 60)
try:
    logger.info("✓ Logging initialized successfully")
    logger.debug("✓ Debug logging works")
    logger.warning("✓ Warning logging works")
    print("✓ Logging framework is working correctly")
    TEST1_PASS = True
except Exception as e:
    print(f"✗ Logging failed: {e}")
    TEST1_PASS = False

# ============== TEST 2: CONFIGURATION ==============
print("\n[TEST 2] Configuration Management")
print("-" * 60)
try:
    print(f"✓ Config LLM timeout: {config.LLM_TIMEOUT}s")
    print(f"✓ Config max suggestions: {config.MAX_OUTFIT_SUGGESTIONS}")
    print(f"✓ Config confidence threshold: {config.CONFIDENCE_CATEGORY_THRESHOLD}")
    print(f"✓ Config fuzzy matching enabled: {config.ENABLE_FUZZY_MATCHING}")
    print("✓ Configuration loaded correctly")
    TEST2_PASS = True
except Exception as e:
    print(f"✗ Configuration failed: {e}")
    TEST2_PASS = False

# ============== TEST 3: INPUT VALIDATION ==============
print("\n[TEST 3] Input Validation")
print("-" * 60)
try:
    # Test valid input
    is_valid, msg = InputValidator.validate_user_text("I have blue jeans")
    assert is_valid, f"Should accept valid text, got: {msg}"
    print("✓ Valid text accepted")
    
    # Test invalid input (too short)
    is_valid, msg = InputValidator.validate_user_text("a")
    assert not is_valid, "Should reject too-short text"
    print("✓ Too-short text rejected")
    
    # Test invalid input (too long)
    is_valid, msg = InputValidator.validate_user_text("x" * 10001)
    assert not is_valid, "Should reject too-long text"
    print("✓ Too-long text rejected")
    
    print("✓ Input validation working correctly")
    TEST3_PASS = True
except AssertionError as e:
    print(f"✗ Validation test failed: {e}")
    TEST3_PASS = False
except Exception as e:
    print(f"✗ Validation error: {e}")
    TEST3_PASS = False

# ============== TEST 4: TEXT PARSER ==============
print("\n[TEST 4] Text Parser")
print("-" * 60)
try:
    # Test garment detection
    result = parse_text_input("I have blue jeans")
    assert result["category"] == "jeans", f"Should detect jeans, got {result['category']}"
    assert result["color"] == "blue", f"Should detect blue, got {result['color']}"
    print("✓ Garment and color detection works")
    
    # Test occasion detection
    result = parse_text_input("I need an outfit for office")
    assert result["occasion"] == "office", f"Should detect office, got {result['occasion']}"
    print("✓ Occasion detection works")
    
    # Test gender detection
    result = parse_text_input("I am male")
    assert result["gender"] == "male", f"Should detect male, got {result['gender']}"
    print("✓ Gender detection works")
    
    print("✓ Text parser working correctly")
    TEST4_PASS = True
except AssertionError as e:
    print(f"✗ Text parser test failed: {e}")
    TEST4_PASS = False
except Exception as e:
    print(f"✗ Text parser error: {e}")
    TEST4_PASS = False

# ============== TEST 5: CONFIDENCE HANDLING ==============
print("\n[TEST 5] Confidence Handling")
print("-" * 60)
try:
    # Test high confidence
    high_conf = {"category": 0.95, "color_primary": 0.88, "pattern": 0.90}
    is_low = is_low_confidence(high_conf)
    assert not is_low, "High confidence should not be flagged as low"
    label = confidence_label(high_conf)
    assert label == "high", f"Should be 'high', got {label}"
    print("✓ High confidence detected correctly")
    
    # Test low confidence
    low_conf = {"category": 0.60, "color_primary": 0.55, "pattern": 0.50}
    is_low = is_low_confidence(low_conf)
    assert is_low, "Low confidence should be flagged"
    label = confidence_label(low_conf)
    assert label == "low", f"Should be 'low', got {label}"
    print("✓ Low confidence detected correctly")
    
    # Test explanations
    explanation = explain_confidence(high_conf)
    assert explanation and "high" in explanation.lower(), "Should explain high confidence"
    print(f"✓ Confidence explanation: {explanation}")
    
    print("✓ Confidence handling working correctly")
    TEST5_PASS = True
except AssertionError as e:
    print(f"✗ Confidence test failed: {e}")
    TEST5_PASS = False
except Exception as e:
    print(f"✗ Confidence error: {e}")
    TEST5_PASS = False

# ============== TEST 6: LLM RESPONSE VALIDATION ==============
print("\n[TEST 6] LLM Response Validation")
print("-" * 60)
try:
    # Test valid response
    valid_response = {
        "final_message": "Here's my recommendation",
        "followup_question": "What else?"
    }
    is_valid, msg = InputValidator.validate_llm_response(valid_response)
    assert is_valid, f"Should accept valid response, got: {msg}"
    print("✓ Valid LLM response accepted")
    
    # Test invalid response (missing field)
    invalid_response = {
        "final_message": "Here's my recommendation"
        # Missing followup_question
    }
    is_valid, msg = InputValidator.validate_llm_response(invalid_response)
    assert not is_valid, "Should reject incomplete response"
    print("✓ Invalid response rejected")
    
    # Test safe validation
    is_valid, msg = safe_validate(InputValidator.validate_llm_response, valid_response)
    assert is_valid, "Safe validation should handle valid input"
    print("✓ Safe validation works")
    
    print("✓ LLM response validation working correctly")
    TEST6_PASS = True
except AssertionError as e:
    print(f"✗ LLM response validation test failed: {e}")
    TEST6_PASS = False
except Exception as e:
    print(f"✗ LLM response validation error: {e}")
    TEST6_PASS = False

# ============== SUMMARY ==============
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

results = [
    ("Logging Framework", TEST1_PASS),
    ("Configuration Management", TEST2_PASS),
    ("Input Validation", TEST3_PASS),
    ("Text Parser", TEST4_PASS),
    ("Confidence Handling", TEST5_PASS),
    ("LLM Response Validation", TEST6_PASS),
]

passed = sum(1 for _, result in results if result)
total = len(results)

for test_name, result in results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status:8} - {test_name}")

print("-" * 60)
print(f"Overall: {passed}/{total} tests passed")

if passed == total:
    print("\n✓✓✓ ALL TESTS PASSED - IMPROVEMENTS WORKING CORRECTLY ✓✓✓")
    sys.exit(0)
else:
    print(f"\n✗✗✗ {total - passed} TEST(S) FAILED - CHECK ERRORS ABOVE ✗✗✗")
    sys.exit(1)
