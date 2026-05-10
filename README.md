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

## 📢 Data Source & Acknowledgements

We explicitly acknowledge and thank the **L3Cube-Pune** team for providing the underlying raw text used in this annotation project.

- **Source Corpus:** [L3Cube-MahaCorpus (news)](https://github.com/l3cube-pune/MarathiNLP)
- **Repository:** [L3Cube-Pune MarathiNLP](https://github.com/l3cube-pune/MarathiNLP)

The raw news articles were sourced from their open-source repository, which acts as a foundational resource for Marathi NLP tasks. Our work builds upon this by adding the layer of semantic coreference annotations.

---

## 📊 Dataset Statistics

The following statistics describe the scale and density of the annotated corpus:

| Metric | Count |
| :--- | :--- |
| **Total Processed Documents** | **490** |
| **Total Sampled Sentences** | **9,994** |
| **Unique Tokens (Vocabulary)** | **5,053** |
| **Annotated Coreference Pairs** | **12,963** |
| **Average Sentence Length** | **29.83 words** |

---

## 🧪 Data Structure & Format

The dataset is provided in **JSON (JavaScript Object Notation)** format, optimized for Hypergraph-based approaches.

### JSON Schema Fields

Each file in the dataset follows this structure:

* **`document_id`**: Unique identifier for the document.
* **`sentences`**: A list containing the raw text of the sentences.
* **`mentions`**: A list of all identified entities (Nouns/Pronouns) with the following metadata:
    * `id`: Unique mention ID.
    * `text`: The surface word (e.g., "पंतप्रधान").
    * `sentence_index`: Index of the sentence containing the mention.
    * `start_char`, `end_char`: Character-level spans of the mention.
* **`clusters`**: A list of coreference chains. Each chain is a list of `mention_ids` that refer to the same underlying entity.

---

## 📂 DataSet Contents

The repository includes:

- `processed_documents/` — Raw Marathi text documents (Sourced from L3Cube-MahaCorpus).
- `annotated_documents/` — Gold-standard coreference annotations in JSON+CoNLL format.
- `schema.md` — Annotation guidelines and tag definitions.

---

## 🎯 Annotation Guidelines

Each document is manually annotated for:
- **Named Entities**
- **Pronouns (explicit + pro-drop)**
- **Nominal mentions**
- **Hyperedges / clusters representing entity chains**

Annotations follow:
- **Gender agreement rules**
- **Number consistency**
- **Semantic context checks**
- **Cross-sentence reference tracking**

A full description of the annotation scheme is provided in `schema.md`.

---

## 🔍 Use Cases

This dataset is suitable for:

- Coreference resolution model training/testing
- Hypergraph-based NLP research
- Benchmarking for low-resource Indian languages
- Linguistic analysis
- Fine-tuning transformer models (e.g., IndicBERT, MahaBERT)

---

## 📜 License

This dataset is released under the **CC BY-NC 4.0 License**
(Non-commercial research usage permitted.)

---

## 🤝 Contributions

If you wish to add more annotations or help expand this corpus, feel free to open an issue or submit a pull request.

---

## 📧 Contact

For questions, collaboration, or academic use cases:

**Mansi Jangle**
Department of Computer Engineering
Pune Institute of Computer Technology

---

## ⭐ Citation

If you use this dataset in academic work, please cite:

Shinde, T., Jangle, M., Bagwan, M.
"Coreference Resolution for Marathi Text Using Hypergraph Method"
PICT, 2025.
