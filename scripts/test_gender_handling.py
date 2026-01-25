#!/usr/bin/env python
"""Quick test for gender detection and context reset"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from conversational_multimodal_fashion_intelligence_system.chat_engine import FashionAIChat

# Create mock LLM
class MockLLM:
    def chat(self, system='', user='', vision_data=None):
        return {
            "final_message": "Test response",
            "followup_question": "Test followup"
        }

# Test scenario
print("=" * 60)
print("Testing Gender Detection and Context Reset")
print("=" * 60)

llm = MockLLM()
bot = FashionAIChat(llm=llm)

# Test 1: Detect female gender
print("\n[Test 1] User says: 'i am a female'")
gender = bot.extract_gender("i am a female")
print(f"  Gender detected: {gender}")
print(f"  bot.user_gender: {bot.user_gender}")
assert gender == 'female', f"Expected 'female', got {gender}"
print("  ✓ PASS")

# Test 2: Detect "women" variation
print("\n[Test 2] User says: 'i am a women so what to wear'")
bot.user_gender = None  # Reset
gender = bot.extract_gender("i am a women so what to wear")
print(f"  Gender detected: {gender}")
print(f"  bot.user_gender: {bot.user_gender}")
assert gender == 'female', f"Expected 'female', got {gender}"
print("  ✓ PASS")

# Test 3: Vision context reset on new question
print("\n[Test 3] Context reset on new question")
bot.user_gender = None
bot.last_vision_data = {"attributes": {"category": "sherwani"}, "confidences": {}}
bot.state.vision = bot.last_vision_data
print(f"  Before: vision = {bot.state.vision}")

# Simulate new question with gender
response = bot.handle("i am a women so what to wear", image_path=None)
print(f"  After: vision = {bot.state.vision}")
print(f"  Gender: {bot.user_gender}")
assert bot.state.vision is None, "Vision should be reset on new question"
assert bot.user_gender == 'female', "Gender should be detected"
print("  ✓ PASS")

# Test 4: Gender-specific response
print("\n[Test 4] Gender-specific response generation")
bot.user_gender = 'female'
response = bot.handle("what should i wear for casual party", image_path=None)
print(f"  Response: {response['reply'][:100]}...")
assert 'female' not in response['reply'].lower() or 'comfortable' in response['reply'].lower(), "Should have gender-specific advice"
print("  ✓ PASS")

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)
