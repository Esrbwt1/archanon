# src/learning/learner.py

from kernel import ArchanonKernel
from sensory.text_parser import TextParser
import spacy # We need spacy here to split text into sentences

class Learner:
    """
    Learner v1.0: The Learning Loop.

    This module orchestrates the process of learning from a text corpus.
    It uses the TextParser to extract knowledge from sentences and then
    instructs the ArchanonKernel to add that knowledge to its MemoryCore.
    """

    def __init__(self, kernel: ArchanonKernel, parser: TextParser):
        """
        Initializes the Learner with a kernel and a text parser.
        
        Args:
            kernel (ArchanonKernel): The cognitive core to populate.
            parser (TextParser): The sensory module for understanding text.
        """
        self.kernel = kernel
        self.parser = parser
        # We use the parser's nlp model for sentence splitting.
        self.nlp = parser.nlp
        print("Learner v1.0 initialized.")

    def learn_from_corpus(self, corpus_filepath: str):
        """
        Reads a text corpus, processes it, and learns facts.

        Args:
            corpus_filepath (str): The path to the text file to learn from.
        """
        print(f"Starting learning process from corpus: {corpus_filepath}")
        try:
            with open(corpus_filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: Corpus file not found at {corpus_filepath}")
            return

        # Use spaCy to split the entire text into sentences
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        
        facts_learned = 0
        for i, sentence in enumerate(sentences):
            if i % 50 == 0 and i > 0:
                print(f"  ...processed {i}/{len(sentences)} sentences. Total facts learned: {facts_learned}")

            triplets = self.parser.extract_triplets(sentence)
            if triplets:
                for subject, relation, obj in triplets:
                    # Instruct the kernel to add the new fact
                    self.kernel.add_fact(subject, obj, relation)
                    facts_learned += 1
        
        print("\nLearning process complete.")
        print(f"Total sentences processed: {len(sentences)}")
        print(f"Total new facts learned: {facts_learned}")
        # We can query the final size of the memory graph as well
        final_node_count = self.kernel.memory._graph.number_of_nodes()
        final_edge_count = self.kernel.memory._graph.number_of_edges()
        print(f"MemoryCore now contains {final_node_count} nodes and {final_edge_count} relationships.")