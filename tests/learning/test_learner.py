# tests/learning/test_learner.py

import pytest
import os
from kernel import ArchanonKernel
from sensory.text_parser import TextParser
from learning.learner import Learner

@pytest.fixture
def learning_setup(tmp_path):
    """
    Creates a full learning setup with a kernel, parser, and a dummy corpus file.
    'tmp_path' is a pytest fixture that provides a temporary directory.
    """
    # Create a dummy corpus file
    corpus_content = "The cat is an animal. An animal is a living thing. The cat is fluffy."
    corpus_file = tmp_path / "test_corpus.txt"
    corpus_file.write_text(corpus_content, encoding="utf-8")
    
    kernel = ArchanonKernel()
    parser = TextParser()
    learner = Learner(kernel, parser)
    
    return learner, kernel, str(corpus_file)

# In tests/learning/test_learner.py

def test_learner_learns_and_kernel_reasons(learning_setup):
    """
    Tests the complete loop with canonicalization.
    """
    learner, kernel, corpus_path = learning_setup
    
    # Check initial state
    assert kernel.ask_question("cat", "animal") is False
    
    # --- The Learning Step ---
    learner.learn_from_corpus(corpus_path)
    
    # --- Verification Step ---
    # 1. Did it learn the canonicalized facts?
    # The nodes should be "cat", "animal", "living thing", NOT "The cat", etc.
    assert kernel.memory._graph.has_node("cat")
    assert kernel.memory._graph.has_node("animal")
    assert kernel.memory._graph.has_node("living thing")
    
    # 2. Can it answer direct questions using canonical entities?
    assert kernel.ask_question("cat", "animal") is True
    assert kernel.ask_question("cat", "fluffy") is True
    
    # 3. The final, most important test: Is the chain of inference now complete?
    assert kernel.ask_question("cat", "living thing") is True