#!/usr/bin/env python3
"""
Regex Pattern Analysis and Verification Test

This test demonstrates the improvement in image path extraction when 
handling multiple image paths in a single message.

Problem: Greedy regex was capturing both paths as a single concatenated string
Solution: Non-greedy regex with path boundary detection separates paths correctly
"""

import re

print("╔" + "="*78 + "╗")
print("║" + " "*22 + "MULTIPLE IMAGE PATH EXTRACTION TEST" + " "*22 + "║")
print("╚" + "="*78 + "╝\n")

# Test cases
test_cases = [
    {
        "name": "Two unquoted Windows paths with spaces",
        "input": r'C:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\manual_testing_images\Screenshot 2026-01-20 165949.png C:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\manual_testing_images\Screenshot 2026-01-20 162743.png i hv these two cloth',
        "expected_count": 2
    },
    {
        "name": "Two quoted paths",
        "input": r'"C:\image1.jpg" "C:\image2.png" which is better?',
        "expected_count": 2
    },
    {
        "name": "Single Windows path with spaces",
        "input": r'C:\Desktop\my outfit.jpg analyze this',
        "expected_count": 1
    },
    {
        "name": "Three consecutive Windows paths",
        "input": r'C:\img1.jpg C:\img2.jpg C:\img3.jpg which one?',
        "expected_count": 3
    },
    {
        "name": "Mixed quoted and unquoted",
        "input": r'"C:\dress1.png" C:\dress2.jpg compare',
        "expected_count": 2
    }
]

def test_pattern(pattern_name, pattern, test_input):
    """Test a regex pattern against input"""
    matches = re.findall(pattern, test_input, re.IGNORECASE)
    return matches

# Define patterns
old_pattern = r'[C-Z]:\\[\w\s\-\.\\/:]*\.(?:jpg|jpeg|png|webp|bmp|gif|avif)'
new_pattern = r'[C-Z]:\\(?:[^:"\n]*?\\)*[^:"\n]*?\.(?:jpg|jpeg|png|webp|bmp|gif|avif)'

print("="*80)
print("REGEX PATTERN ANALYSIS")
print("="*80)

print("\nOld Pattern (GREEDY):")
print(f"  {old_pattern}")
print("  Issues: Uses [\\w\\s\\-\\.\\\\/:]*  which matches EVERYTHING until last extension")

print("\nNew Pattern (NON-GREEDY):")
print(f"  {new_pattern}")
print("  Improvements: Uses [^:\"\\n]*? which stops at drive letters/quotes/newlines")

print("\n" + "="*80)
print("TESTING: Multiple Image Path Extraction")
print("="*80 + "\n")

all_passed = True

for i, test_case in enumerate(test_cases, 1):
    print(f"Test {i}: {test_case['name']}")
    print("-" * 80)
    
    print(f"Input: {test_case['input'][:75]}{'...' if len(test_case['input']) > 75 else ''}")
    
    # Test with old pattern
    old_matches = test_pattern("old", old_pattern, test_case['input'])
    print(f"\nOld Pattern Results:")
    print(f"  Matches: {len(old_matches)}")
    if old_matches:
        for j, match in enumerate(old_matches, 1):
            display = match if len(match) < 50 else match[:47] + "..."
            print(f"    {j}. {display} (len: {len(match)})")
    
    # Test with new pattern
    new_matches = test_pattern("new", new_pattern, test_case['input'])
    print(f"\nNew Pattern Results:")
    print(f"  Matches: {len(new_matches)}")
    if new_matches:
        for j, match in enumerate(new_matches, 1):
            display = match if len(match) < 50 else match[:47] + "..."
            print(f"    {j}. {display} (len: {len(match)})")
    
    # Verify
    passed = len(new_matches) == test_case['expected_count']
    
    if passed:
        print(f"\n✅ PASS: Expected {test_case['expected_count']}, got {len(new_matches)}")
    else:
        print(f"\n❌ FAIL: Expected {test_case['expected_count']}, got {len(new_matches)}")
        all_passed = False
    
    print()

print("="*80)
print("ANALYSIS: Why Old Pattern Fails")
print("="*80)
print("""
The old pattern:  [C-Z]:\\[\\w\\s\\-\\.\\\\/:]*\\.(?:jpg|...)

When parsing:  'path1.png C:\\path2.png'
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
               
The [\\w\\s\\-\\.\\\\/:]*  part is GREEDY and matches:
  - All word characters: path1
  - ALL spaces and special chars: path1.png C:\\ 
  - More word chars: path2
  - Until hitting the LAST .png extension

Result: Entire string treated as ONE path (WRONG!)

The new pattern:  [C-Z]:\\(?:[^:\"\\n]*?\\)*[^:\"\\n]*?\\.(?:jpg|...)

Uses [^:\"\\n]*?  which is NON-GREEDY and stops at:
  - Another drive letter (:)
  - Quote character (\")
  - Newline (\\n)

This allows it to:
  1. Match from C:\\ to first .png
  2. Stop at the C: in second path
  3. Continue and match second path to its .png
  
Result: TWO paths correctly separated (CORRECT!)
""")

print("="*80)
print("SUMMARY")
print("="*80)

if all_passed:
    print(f"\n✅ All {len(test_cases)} tests PASSED!")
    print("\nKey Improvements:")
    print("  ✓ Non-greedy matching prevents capturing multiple paths as one")
    print("  ✓ Path boundary detection with [^:\"\\n]* patterns")
    print("  ✓ Correctly handles 2+ images in single message")
    print("  ✓ Works with quoted and unquoted paths")
    print("  ✓ Preserves backward compatibility with single images")
else:
    print(f"\n❌ Some tests failed!")

print("\n" + "="*80)
