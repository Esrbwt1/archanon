# tools/run_learning_demo.py

import sys
import os

# This is a bit of a hack to make sure the script can find the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kernel import ArchanonKernel
from sensory.text_parser import TextParser
from learning.learner import Learner

def main():
    """
    A live demonstration of the ARCHANON Phase 2 learning capabilities.
    """
    print("--- INITIALIZING ARCHANON KERNEL v1.0 ---")
    kernel = ArchanonKernel()
    parser = TextParser()
    learner = Learner(kernel, parser)

    print("\n--- BEGINNING LEARNING FROM CORPUS ---")
    corpus_path = "data_corpus/simple_wiki_corpus_v1.txt"
    learner.learn_from_corpus(corpus_path)

    print("\n--- KNOWLEDGE INTERROGATION ---")
    print("Let's see what the kernel has learned...")

    # We will ask it questions we expect it might be able to answer
    # based on the first 100 articles of Simple Wikipedia.
    queries = [
        ("albert einstein", "physicist"), # is_a
        ("germany", "country"),          # is_a
        ("apple inc.", "company"),        # is_a
        ("computer", "machine"),         # is_a
        ("albert einstein", "german-born"), # has_property (might be tricky)
        ("albert einstein", "person")      # multi-step inference?
    ]

    for subject, prop in queries:
        result = kernel.ask_question(subject, prop)
        print(f"Q: Is '{subject}' a '{prop}'?  ->  A: {result}")
    
    print("\n--- DEMONSTRATION COMPLETE ---")
    print("To see the full reasoning, inspect the Chain of Consciousness log if desired.")
    # print(kernel.get_reasoning_trace()) # Uncomment to see the very long log

if __name__ == "__main__":
    main()