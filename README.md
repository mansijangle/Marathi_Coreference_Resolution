# 🧠 Marathi Coreference Resolution using Hypergraphs

This project performs coreference resolution in Marathi using a **hypergraph-based approach**.

It works in the following steps:

1. Mention Detection: All possible noun/pronoun mentions are extracted from each sentence.
2. 🧬 Gender Detection with Suffix Rules : Gender is predicted using common Marathi suffix patterns (like `-ई`, `-का`, `-श`) and Stanza-based linguistic analysis for accurate classification of unknown names.
3. Similarity Scoring: Each mention pair is assigned a similarity score based on:
   - Gender match  
   - Lexical overlap  
   - Exact word match  
   - Pronoun boosting
4. Hyperedge Construction: All related mentions with high similarity scores are connected via **hyperedges**.
5. Clustering: Pairs with relation and high scores (not just the maximum) are grouped together to form coreference clusters.

This method allows resolving pronouns like "तो", "तिने", or "त्यांनी" back to the correct noun (e.g., "राम", "सारिका", "मित्रांनी") using both **linguistic signals and graph-based relationships**.

Example : 
Step 1: Gender Detection
- `सारिकाने` → female
- `तिने` → female

Step 2: Hyperedge Creation
- `{'सारिकाने', 'तिने'}` → Score: 2.0 (gender + pronoun boost)
- `{'तिने', 'बनवले'}` → Score: 0.6
- ...

Step 3: Clustering
- Top cluster pair: `तिने ↔ सारिकाने` (Score: 2.0)
- This is used to resolve that "तिने" refers to "सारिकाने"


 Final output : सारिकाने जेवण बनवले, तिने चांगले जेवण बनवले.

---

👩‍💻 Contributors

- Mansi Jangle – Core idea and model development  
- Tanishq Shinde – Logic implementation and testing  
- Misbah Bagwan – Support in model design and evaluation


⚠️ Note: This project is currently under development. 
Our team is actively working on improving the algorithm and verifying results.
