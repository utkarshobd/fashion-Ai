"""
Tests for Fashion Classifier
"""

import pytest
from pathlib import Path
from src.classifier import FashionClassifier

def test_classifier_initialization():
    """Test classifier can be initialized"""
    classifier = FashionClassifier()
    assert classifier.schema is not None

def test_get_categories():
    """Test getting categories from schema"""
    classifier = FashionClassifier()
    categories = classifier.get_categories()
    
    assert "ethnic" in categories
    assert "western" in categories
    assert "kurta" in categories["ethnic"]
    assert "shirt" in categories["western"]

def test_get_attributes():
    """Test getting attributes from schema"""
    classifier = FashionClassifier()
    attributes = classifier.get_attributes()
    
    assert "shared" in attributes
    assert "sleeve_length" in attributes["shared"]