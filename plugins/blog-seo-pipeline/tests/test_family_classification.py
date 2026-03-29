from __future__ import annotations

from scripts.family_classification import classify_family
from scripts.job_state import JobState


def test_classify_deep_dive_guide():
    family, confidence = classify_family(JobState(format="deep-dive-guide", brief="anfaenger"))

    assert family == "deep-dive-guide"
    assert confidence == "high"


def test_classify_product_comparison():
    family, confidence = classify_family(JobState(format="comparison", brief="vergleich"))

    assert family == "product-comparison"
    assert confidence == "high"


def test_classify_curation_listicle():
    family, confidence = classify_family(JobState(format="listicle", brief="rank the best kits"))

    assert family == "curation-listicle"
    assert confidence == "high"
