# Hindi/Marathi coreference resolution with pronoun prioritization


# Marathi references for pronouns
import stanza
import unicodedata
from collections import defaultdict

# Initialize Stanza pipeline
nlp = stanza.Pipeline('mr', processors='tokenize,mwt,pos,lemma,depparse,ner')

def guess_gender(word_text):
    """Enhanced gender detection combining rules and Stanza features"""
    word = unicodedata.normalize('NFC', word_text.strip())
    male_suffixes = ['अ', 'य', 'श', 'न', 'ध', 'ल', 'नंद', 'उ', 'ऊ', 'त', 'र', 'ष्णु', 'षि', 'जी', 'ती']
    female_suffixes = ['इ', 'ई', 'आ', 'ा', 'ी', 'धि','नी','का','नी']

    if any(word.endswith(suffix) for suffix in male_suffixes):
        return "male"
    elif any(word.endswith(suffix) for suffix in female_suffixes):
        return "female"
    return "neutral"
# ---------------------- Similarity Score -----------------------
def similarity_score(w1, w2):
    gender1 = get_gender(w1)
    gender2 = get_gender(w2)
    score = 0.0
    if gender1 == gender2:
        score += 0.9
    if w1 == w2:
        score += 0.9
    if len(set(w1) & set(w2)) > 0:
        score += 0.2
    return round(score, 2)

# ---------------------- Coreference Resolution HyperGraph  ----------------------
def coreference_resolution(sentences):
    all_results = []

    for idx, sentence in enumerate(sentences, 1):
        mentions = extract_mentions(sentence)
        local_edges = []
        used_pronouns = set()
        seen_edges = set()
        main_noun = mentions[0] if mentions else None

        for i in range(len(mentions)):
            m1 = mentions[i]

            # Pronoun priority handling
            if m1 in marathi_references and m1 not in used_pronouns:
                candidates = []
                for j in range(len(mentions)):
                    m2 = mentions[j]
                    if m2 != m1:
                        score = similarity_score(m1, m2)
                        score += 0.9  # Pronoun boost
                        candidates.append((set([m1, m2]), round(score, 2)))

                candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
                if candidates:
                    top_edge, top_score = candidates[0]
                    if len(top_edge) >= 2:
                        edge_tuple = tuple(sorted(top_edge))
                        if edge_tuple not in seen_edges:
                            local_edges.append((top_edge, top_score))
                            seen_edges.add(edge_tuple)

                    # Other candidates with downgraded score
                    for edge, sc in candidates[1:]:
                        downgraded_score = round(sc - 0.5, 2)
                        if downgraded_score >= 0.5:
                            edge_tuple = tuple(sorted(edge))
                            if edge_tuple not in seen_edges:
                                local_edges.append((edge, downgraded_score))
                                seen_edges.add(edge_tuple)

                # Extra boost: Pronoun → main noun
                if main_noun and main_noun != m1:
                    edge = set([main_noun, m1])
                    edge_tuple = tuple(sorted(edge))
                    if edge_tuple not in seen_edges:
                        local_edges.append((edge, 1.4))
                        seen_edges.add(edge_tuple)

                used_pronouns.add(m1)

            # Normal noun-noun matching
            for j in range(i + 1, len(mentions)):
                m2 = mentions[j]
                if m1 not in marathi_references and m2 not in marathi_references:
                    score = similarity_score(m1, m2)
                    if score >= 0.5:
                        edge = set([m1, m2])
                        edge_tuple = tuple(sorted(edge))
                        if edge_tuple not in seen_edges:
                            local_edges.append((edge, score))
                            seen_edges.add(edge_tuple)

        all_results.append((sentence, local_edges))

    return all_results

# ---------------------- Clustering with Highest Score----------------------
def extract_pairs_from_edges(edges):
    pairs = []
    for edge, score in edges:
        edge_list = list(edge)
        if len(edge_list) == 2:
            pairs.append((edge_list[0], edge_list[1], score))
    return pairs

# ---------------------- Running ----------------------
results = coreference_resolution(sentences)

print("🧠 Sentence-wise Coreference Hyperedges with Priority:\n")

for idx, (sentence, edges) in enumerate(results, 1):
    print(f"📌 Sentence {idx}: {sentence}")
    if not edges:
        print("   No coreference hyperedges found.")
    else:
        for edge, score in edges:
            print(f"   ➤ Hyperedge: {edge}, Similarity Score: {score}")

    # Auto extracting pairs from hyperedges
    pairs = extract_pairs_from_edges(edges)
    if pairs:
        print("Cluster Pairs:")
        for p1, p2, score in pairs:
            print(f"      ➡ {p1} - {p2} (Score: {score})")
    print()


sentences = [
    "सारिकाने जेवण बनवले, तिने चांगले जेवण बनवले.",
    "मित्रांनी भेट घेतली, त्यांनी खूप मजा केली.",
     "राम शाळेत जातो तो हुशार आहे",
    "मित्रांनी सहल आखली. त्यांनी खूप मजा केली",

]




Output :🧠 Sentence-wise Coreference Hyperedges with Priority:

📌 Sentence 1: सारिकाने जेवण बनवले, तिने चांगले जेवण बनवले.
   ➤ Hyperedge: {'जेवण', 'बनवले'}, Similarity Score: 1.1
   ➤ Hyperedge: {'चांगले', 'जेवण'}, Similarity Score: 1.1
   ➤ Hyperedge: {'जेवण'}, Similarity Score: 2.0
   ➤ Hyperedge: {'चांगले', 'बनवले'}, Similarity Score: 1.1
   ➤ Hyperedge: {'बनवले'}, Similarity Score: 2.0
   ➤ Hyperedge: {'तिने', 'सारिकाने'}, Similarity Score: 2.0
   ➤ Hyperedge: {'तिने', 'जेवण'}, Similarity Score: 0.6
   ➤ Hyperedge: {'तिने', 'बनवले'}, Similarity Score: 0.6
   ➤ Hyperedge: {'तिने', 'चांगले'}, Similarity Score: 0.6
   🔗 Extracted Pairs:
      ➡ जेवण - बनवले (Score: 1.1)
      ➡ चांगले - जेवण (Score: 1.1)
      ➡ चांगले - बनवले (Score: 1.1)
      ➡ तिने - सारिकाने (Score: 2.0)
      ➡ तिने - जेवण (Score: 0.6)
      ➡ तिने - बनवले (Score: 0.6)
      ➡ तिने - चांगले (Score: 0.6)

📌 Sentence 2: मित्रांनी भेट घेतली, त्यांनी खूप मजा केली.
   ➤ Hyperedge: {'मित्रांनी', 'भेट'}, Similarity Score: 0.9
   ➤ Hyperedge: {'घेतली', 'मित्रांनी'}, Similarity Score: 1.1
   ➤ Hyperedge: {'केली', 'मित्रांनी'}, Similarity Score: 1.1
   ➤ Hyperedge: {'घेतली', 'भेट'}, Similarity Score: 1.1
   ➤ Hyperedge: {'केली', 'भेट'}, Similarity Score: 1.1
   ➤ Hyperedge: {'घेतली', 'केली'}, Similarity Score: 1.1
   ➤ Hyperedge: {'मित्रांनी', 'त्यांनी'}, Similarity Score: 2.0
   ➤ Hyperedge: {'घेतली', 'त्यांनी'}, Similarity Score: 1.5
   ➤ Hyperedge: {'केली', 'त्यांनी'}, Similarity Score: 1.5
   ➤ Hyperedge: {'त्यांनी', 'भेट'}, Similarity Score: 1.3
   🔗 Extracted Pairs:
      ➡ मित्रांनी - भेट (Score: 0.9)
      ➡ घेतली - मित्रांनी (Score: 1.1)
      ➡ केली - मित्रांनी (Score: 1.1)
      ➡ घेतली - भेट (Score: 1.1)
      ➡ केली - भेट (Score: 1.1)
      ➡ घेतली - केली (Score: 1.1)
      ➡ मित्रांनी - त्यांनी (Score: 2.0)
      ➡ घेतली - त्यांनी (Score: 1.5)
      ➡ केली - त्यांनी (Score: 1.5)
      ➡ त्यांनी - भेट (Score: 1.3)

📌 Sentence 3: राम शाळेत जातो तो हुशार आहे
   ➤ Hyperedge: {'जातो', 'शाळेत'}, Similarity Score: 1.1
   ➤ Hyperedge: {'शाळेत', 'हुशार'}, Similarity Score: 1.1
   ➤ Hyperedge: {'जातो', 'हुशार'}, Similarity Score: 1.1
   ➤ Hyperedge: {'राम', 'तो'}, Similarity Score: 1.8
   ➤ Hyperedge: {'शाळेत', 'तो'}, Similarity Score: 0.6
   ➤ Hyperedge: {'जातो', 'तो'}, Similarity Score: 0.6
   🔗 Extracted Pairs:
      ➡ जातो - शाळेत (Score: 1.1)
      ➡ शाळेत - हुशार (Score: 1.1)
      ➡ जातो - हुशार (Score: 1.1)
      ➡ राम - तो (Score: 1.8)
      ➡ शाळेत - तो (Score: 0.6)
      ➡ जातो - तो (Score: 0.6)

📌 Sentence 4: मित्रांनी सहल आखली. त्यांनी खूप मजा केली
   ➤ Hyperedge: {'सहल', 'मित्रांनी'}, Similarity Score: 0.9
   ➤ Hyperedge: {'आखली', 'मित्रांनी'}, Similarity Score: 1.1
   ➤ Hyperedge: {'केली', 'मित्रांनी'}, Similarity Score: 1.1
   ➤ Hyperedge: {'सहल', 'आखली'}, Similarity Score: 1.1
   ➤ Hyperedge: {'सहल', 'केली'}, Similarity Score: 1.1
   ➤ Hyperedge: {'आखली', 'केली'}, Similarity Score: 1.1
   ➤ Hyperedge: {'मित्रांनी', 'त्यांनी'}, Similarity Score: 2.0
   ➤ Hyperedge: {'आखली', 'त्यांनी'}, Similarity Score: 1.5
   ➤ Hyperedge: {'केली', 'त्यांनी'}, Similarity Score: 1.5
   ➤ Hyperedge: {'सहल', 'त्यांनी'}, Similarity Score: 1.3
   🔗 Extracted Pairs:
      ➡ सहल - मित्रांनी (Score: 0.9)
      ➡ आखली - मित्रांनी (Score: 1.1)
      ➡ केली - मित्रांनी (Score: 1.1)
      ➡ सहल - आखली (Score: 1.1)
      ➡ सहल - केली (Score: 1.1)
      ➡ आखली - केली (Score: 1.1)
      ➡ मित्रांनी - त्यांनी (Score: 2.0)
      ➡ आखली - त्यांनी (Score: 1.5)
      ➡ केली - त्यांनी (Score: 1.5)
      ➡ सहल - त्यांनी (Score: 1.3)
