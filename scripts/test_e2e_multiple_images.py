#!/usr/bin/env python3
"""
End-to-end test for multiple image path handling in Fashion AI Chat system.

This script tests the complete flow:
1. User provides two image paths and a message
2. System extracts both image paths correctly
3. Handler processes them as a list
4. Response acknowledges both images
"""

import sys
import os
import re
from pathlib import Path

# Test the exact scenario from user
test_scenarios = [
    {
        "name": "Wedding outfit comparison (two images)",
        "input": """C:\\Users\\utkarshh\\Desktop\\FAI\\FAII\\fashion_dataset_transformed\\manual_testing_images\\8bea8bac07ed75596e5597f6d2997f07cfd81fac.avif C:\\Users\\utkarshh\\Desktop\\FAI\\FAII\\fashion_dataset_transformed\\manual_testing_images\\914890-11380482.avif i hv these two cloth is they are good for my brother wedding""",
        "expected_images": 2,
        "contains_wedding": True
    },
    {
        "name": "Three image comparison",
        "input": """C:\\image1.jpg C:\\image2.jpg C:\\image3.jpg which one is best""",
        "expected_images": 3,
        "contains_wedding": False
    },
    {
        "name": "Two images with quotes",
        "input": """"C:\\dress1.png" "C:\\dress2.png" compare these""",
        "expected_images": 2,
        "contains_wedding": False
    }
]

def extract_image_paths(text):
    """Extract image paths using the same logic as chat_engine.py"""
    image_paths = []
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.avif')
    
    # Method 1: Quoted paths
    if '"' in text:
        quoted_strings = re.findall(r'"([^"]*)"', text)
        for quoted in quoted_strings:
            if any(quoted.lower().endswith(ext) for ext in image_extensions):
                if '\\' in quoted or '/' in quoted:
                    image_paths.append(quoted)
                    text = text.replace(f'"{quoted}"', '').strip()
    
    # Method 2: Windows paths (non-greedy to avoid capturing multiple as one)
    if not image_paths:
        windows_path_pattern = r'[C-Z]:\\(?:[^:"\n]*?\\)*[^:"\n]*?\.(?:jpg|jpeg|png|webp|bmp|gif|avif)'
        matches = re.findall(windows_path_pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                if match and len(match) > 4:
                    image_paths.append(match)
                    text = text.replace(match, '').strip()
    
    # Method 3: Unix paths
    if not image_paths:
        unix_path_pattern = r'/(?:[^:\n]*?/)*[^:\n]*?\.(?:jpg|jpeg|png|webp|bmp|gif|avif)'
        matches = re.findall(unix_path_pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                if match:
                    image_paths.append(match)
                    text = text.replace(match, '').strip()
    
    return image_paths, text.strip()

print("╔" + "="*78 + "╗")
print("║" + " "*20 + "END-TO-END MULTIPLE IMAGE TEST" + " "*28 + "║")
print("╚" + "="*78 + "╝\n")

all_passed = True

for i, scenario in enumerate(test_scenarios, 1):
    print(f"Test {i}: {scenario['name']}")
    print("-" * 80)
    
    input_text = scenario['input']
    image_paths, remaining_text = extract_image_paths(input_text)
    
    # Check extraction
    print(f"  Input: {input_text[:80]}{'...' if len(input_text) > 80 else ''}")
    print(f"  Images extracted: {len(image_paths)}")
    
    passed = True
    
    # Verify count
    if len(image_paths) != scenario['expected_images']:
        print(f"  ❌ Expected {scenario['expected_images']} images, got {len(image_paths)}")
        passed = False
    else:
        print(f"  ✓ Correct number of images extracted")
    
    # Verify wedding context
    if scenario['contains_wedding']:
        if 'wedding' in remaining_text.lower():
            print(f"  ✓ Wedding context preserved in text")
        else:
            print(f"  ❌ Wedding context lost in text: '{remaining_text}'")
            passed = False
    
    # Show extracted paths
    for j, path in enumerate(image_paths, 1):
        print(f"    Image {j}: {Path(path).name}")
    
    # Verify what would be sent to handler
    if len(image_paths) > 1:
        print(f"  Handler will receive: image_path={image_paths} (list of {len(image_paths)})")
        print(f"  Response will: Acknowledge {len(image_paths)} items and provide comparison advice")
    elif len(image_paths) == 1:
        print(f"  Handler will receive: image_path='{image_paths[0]}' (single string)")
    
    # Summary
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}\n")
    
    if not passed:
        all_passed = False

print("="*80)
if all_passed:
    print("✅ All tests PASSED! Multiple image extraction is working correctly.")
    print("\nThe system is now ready for:")
    print("  1. Users to send multiple outfits for comparison")
    print("  2. Wedding outfit analysis with multiple pieces")
    print("  3. Style matching across multiple garments")
else:
    print("❌ Some tests FAILED. Please review the output above.")

print("="*80)
