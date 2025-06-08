# ARCHANON Learning Curriculum v1: Text-Based Knowledge Extraction

This document outlines the initial curriculum for training the Archanon Kernel using a text-based corpus (e.g., Simple Wikipedia). The goal is to populate the `MemoryCore` with structured knowledge derived from unstructured sentences.

The learning process is divided into tiers, starting with the most fundamental and reliable information first.

---

## Phase 2 Objective

To build a "Learning Loop" that can:
1.  Read a sentence from the corpus.
2.  Parse the sentence to identify potential facts.
3.  Add those facts as nodes and relationships to the `MemoryCore`.

---

## Tier 1: Foundational Entities & "is_a" Relationships

**Priority:** Highest. This tier establishes the fundamental ontology of the knowledge graph.

**Target Patterns:** Sentences that define the type or class of a noun. We will search for specific linguistic markers.

*   **Primary Marker:** `[Noun Phrase 1] + is a/an + [Noun Phrase 2]`
    *   *Example:* "A cat is an animal."
    *   *Resulting Fact:* `memory.add_relationship("cat", "animal", "is_a")`

*   **Secondary Marker:** `[Noun Phrase 1] + is the + [Role]`
    *   *Example:* "Paris is the capital of France."
    *   *Resulting Fact:* `memory.add_relationship("Paris", "capital of France", "is_a")` (Note: "capital of France" becomes a single concept node).

**Goal:** To build a robust hierarchy of `is_a` relationships, which is critical for the `CausalEngine`'s deduction capabilities.

---

## Tier 2: Descriptive Properties & "has_property" / "has_attribute" Relationships

**Priority:** Medium. This tier adds descriptive richness to the entities established in Tier 1.

**Target Patterns:** Sentences that describe the attributes of a noun.

*   **Primary Marker:** `[Noun Phrase] + is + [Adjective/Noun]`
    *   *Example:* "The sky is blue."
    *   *Resulting Fact:* `memory.add_relationship("sky", "blue", "has_property")`
    *   *Example:* "Water is a liquid."
    *   *Resulting Fact:* `memory.add_relationship("water", "liquid", "has_attribute")`

**Goal:** To enrich the knowledge graph with factual attributes, allowing for more detailed queries in the future.

---

## Implementation Note

The initial implementation will rely on simple pattern matching (e.g., using regular expressions or basic NLP sentence splitting). It will not be perfect, but it will serve as the baseline for this "sensory system." Future versions will incorporate more sophisticated Natural Language Processing (NLP) techniques.