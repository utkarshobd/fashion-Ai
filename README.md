# Fashion AI Project Overview

This document explains the complete architecture of the Fashion AI project and how its components interact. It is designed to help you understand the structure, technology choices, and the workflow from data to final recommendation.
# This repository contains partial code only. The full codebase and raw dataset are not included here to protect execution rights and intellectual property, as they are available for purchase.  

---

## 🎯 Project Problem Statement 

The system aims to:

1. Understand clothing attributes from images and/or text.
2. Recommend outfits intelligently based on user intent and context.
3. Explain recommendations and handle mistakes gracefully.
4. Adapt to real-world user behavior (gender, occasion, preferences).

The project combines a vision model, a reasoning LLM, and structured fashion rules.

---

## 🧩 High-Level Architecture

```
User Input
│
├── Image
├── Text
└── Image + Text
        ↓
────────────────────────────
VISION UNDERSTANDING LAYER
────────────────────────────
• Multi-head CNN
• Structural attributes
• CLIP verification
• Confidence scoring
        ↓
────────────────────────────
FASHION NORMALIZATION LAYER
────────────────────────────
• Error correction
• Attribute cleanup
• Semantic merging
        ↓
────────────────────────────
OUTFIT INTELLIGENCE ENGINE
────────────────────────────
• Outfit graph
• Compatibility rules
• Occasion logic
• Climate logic
        ↓
────────────────────────────
LLM REASONING ENGINE
────────────────────────────
• Explanation
• Fallback correction
• Text-only reasoning
• Confidence recovery
        ↓
Final Recommendation
```

Each stage enriches or validates the data before passing it along.

---

## 🔍 Vision Model (CNN)

- Implemented in `training_system/model.py`.
- Backbone: **EfficientNet-B0** pretrained on ImageNet.
- Five classification heads produce attributes: `category`, `sub_category`, `color_primary`, `pattern`, `sub_class`.
- Training scripts and data handling are in `training_system/` and `training_system_v2/`.
- Outputs are multi‑head predictions and the architecture supports freezing/unfreezing layers for fine‑tuning.

Typical usage:

```python
from model import MultiHeadFashionModel
model = MultiHeadFashionModel().to(DEVICE)
```

- Checkpoints stored under `training_system/checkpoints/`.

---

## 🗃 Data & Annotation

- Raw images in `images_original/` and `accessories_original/`.
- Resized versions under `images_resized512/` and `accessories_resized512/`.
- Label files (`annotations/labels_*.csv`); v2 scripts assist in cleaning and enhancing data.
- Annotation utilities exist (`annotation_v2/create_enhanced_annotations.py`, `update_length_mapping.py`, etc.).

---

## ⚙️ Recommendation Engine

Located in `recommendation_architecture/` with these key modules:

- `confidence_handler.py` – handles uncertain predictions and CLIP scores.
- `rule_engine.py` & `occasion_engine.py` – apply domain knowledge for outfit compatibility.
- `outfit_generator.py` – builds outfit suggestions from normalized attributes.
- `recommender.py` – integrates all components and produces final suggestions.
- Support utilities: `text_parser.py`, `schemas.py`, `utils.py`.

The Markdown file `whole_structure_recommendation.md` contains a detailed narrative of this architecture.

---

## 💬 Conversational System

The chat‑based frontend lives in `conversational_multimodal_fashion_intelligence_system/`.

Key files:

- `chat_engine.py` – core conversation handler; tracks state, calls vision and LLM, manages gender extraction and context.
- `llm_reasoner.py` – constructs prompts, calls the LLM, parses/validates responses.
- `config.py` – central configuration, including LLM settings and thresholds.
- `validators.py` – input validation (image paths, LLM output, etc.).

Other helpers: `state.py`, `logger.py`, `prompts.py`, `fashion_expertise.py`.

---

## 🧠 LLM Integration

The project uses a language model to reason about fashion attributes and deliver natural responses.

- **Model**: **Mistral‑7B** (configurable via `LLM_MODEL_NAME`, `LLM_MODEL_PATH` in `config.py`).
- The LLM's interface is expected to have a `chat(system, user, vision_data)` method; tests use a `MockLLM` with the same API.
- Responses are parsed and validated; fallback logic ensures graceful degradation if the LLM fails.
- Vision data (attributes/confidences) are optionally passed along for multimodal reasoning.

Typical prompt flow (see `prompts.py`):

1. System prompt defines role/behavior.
2. User prompt template injects vision output and conversation history.
3. `llm_reasoner.reason()` handles the call and returns structured actions like `recommend`, `ask`, `correct`, `explain`.

---

## ✅ Testing & Utilities

- Unit tests under `tests/` validate the classifier and accuracy (e.g. `test_accuracy.py`).
- Many standalone scripts in `scripts/` exercise features like multi‑image chat, gender handling, or LLM improvements.
- Logging and configuration allow easy debugging and tuning.

---

## 🛠 How to Get Started

1. **Environment**: activate `.venv`, install dependencies from `requirements.txt` (both root and sub‑folders as needed).
2. **Data preparation**: run annotation scripts to produce cleaned label CSVs. Resize images if necessary.
3. **Training**: use `training_system/train.py` or `training_system_v2/main.py` to train the CNN; monitor with logging and save checkpoints.
4. **Inference**: load a checkpoint in `src/classifier.py` or import `MultiHeadFashionModel` directly.
5. **Chat**: instantiate an LLM client (real or mock) and pass it to `FashionAIChat`; feed user inputs and images to test the end‑to‑end flow.

---

## 📌 Takeaways

- The project is a **hybrid multimodal system**: structured vision model + LLM + rule‑based engine.
- **EfficientNet-B0** is used for the CNN; the model is multi‑headed to produce several attribute predictions simultaneously.
- **Mistral‑7B** is the LLM of choice, configured in `config.py` and used via the reasoning module.
- Comprehensive architecture is documented in `recommendation_architecture/whole_structure_recommendation.md`.
- Tests and scripts provide examples of using the system in both development and manual testing contexts.

Happy learning! Study each module in sequence and run the scripts to see the pipeline in action.

---

*This file can act as your cheat sheet while you explore the Fashion AI repository.*
