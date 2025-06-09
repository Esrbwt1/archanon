# In src/sensory/text_parser.py

import spacy
from typing import List, Tuple, Optional

class TextParser:
    """
    TextParser v1.3: Canonicalization.

    This version adds entity canonicalization to ensure that different phrases
    referring to the same concept (e.g., "a cat", "The cat") are resolved
    to a single, standard representation (e.g., "cat").
    """

    def __init__(self):
        """Initializes the parser by loading a spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("TextParser v1.3 initialized with 'en_core_web_sm' model.")
        except OSError:
            print("spaCy model 'en_core_web_sm' not found.")
            print("Please run: python -m spacy download en_core_web_sm")
            self.nlp = None

    def _canonicalize_entity(self, phrase: str) -> str:
        """Converts a phrase to its canonical form."""
        phrase = phrase.lower().strip()
        articles = ["a ", "an ", "the "]
        for article in articles:
            if phrase.startswith(article):
                phrase = phrase[len(article):]
        return phrase.strip()

    def extract_triplets(self, sentence: str) -> List[Tuple[str, str, str]]:
        """
        Parses a single sentence and extracts knowledge triplets.
        Now returns canonicalized entities.
        """
        if not self.nlp:
            return []

        doc = self.nlp(sentence.strip())
        triplets = []

        for token in doc:
            if token.lemma_ == "be":
                subjects = [child for child in token.children if child.dep_ == "nsubj"]
                attributes = [child for child in token.children if child.dep_ in ("attr", "acomp")]

                if subjects and attributes:
                    subject_phrase = " ".join(t.text for t in subjects[0].subtree).strip()
                    attribute_phrase = " ".join(t.text for t in attributes[0].subtree).strip()

                    is_a_candidate = False
                    if attributes[0].pos_ == "NOUN":
                        is_a_candidate = True
                    first_child_of_attr = next(attributes[0].children, None)
                    if first_child_of_attr and first_child_of_attr.pos_ == "DET":
                        is_a_candidate = True
                    
                    if is_a_candidate:
                        # Apply canonicalization
                        canonical_subject = self._canonicalize_entity(subject_phrase)
                        canonical_object = self._canonicalize_entity(attribute_phrase)
                        triplets.append((canonical_subject, "is_a", canonical_object))
                    
                    elif attributes[0].pos_ == "ADJ":
                        # Apply canonicalization
                        canonical_subject = self._canonicalize_entity(subject_phrase)
                        canonical_object = self._canonicalize_entity(attribute_phrase)
                        triplets.append((canonical_subject, "has_property", canonical_object))

        return self._clean_triplets(triplets) # _clean_triplets still useful for deduplication
    
    def _clean_triplets(self, triplets: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """A helper to remove duplicates and clean up text."""
        # This function is now simpler as canonicalization handles most of the work.
        return list(set(triplets)) # Use set for efficient deduplication