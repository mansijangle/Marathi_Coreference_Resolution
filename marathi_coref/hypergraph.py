from .mention_detection import extract_mentions
from .similarity import similarity_score
from .constants import marathi_references

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

                        score += 0.9

                        candidates.append(
                            (set([m1, m2]), round(score, 2))
                        )

                candidates = sorted(
                    candidates,
                    key=lambda x: x[1],
                    reverse=True
                )

                if candidates:

                    top_edge, top_score = candidates[0]

                    if len(top_edge) >= 2:

                        edge_tuple = tuple(sorted(top_edge))

                        if edge_tuple not in seen_edges:

                            local_edges.append(
                                (top_edge, top_score)
                            )

                            seen_edges.add(edge_tuple)

                    for edge, sc in candidates[1:]:

                        downgraded_score = round(sc - 0.5, 2)

                        if downgraded_score >= 0.5:

                            edge_tuple = tuple(sorted(edge))

                            if edge_tuple not in seen_edges:

                                local_edges.append(
                                    (edge, downgraded_score)
                                )

                                seen_edges.add(edge_tuple)

                # Extra boost
                if main_noun and main_noun != m1:

                    edge = set([main_noun, m1])

                    edge_tuple = tuple(sorted(edge))

                    if edge_tuple not in seen_edges:

                        local_edges.append((edge, 1.4))

                        seen_edges.add(edge_tuple)

                used_pronouns.add(m1)

            # Normal noun matching
            for j in range(i + 1, len(mentions)):

                m2 = mentions[j]

                if (
                    m1 not in marathi_references
                    and
                    m2 not in marathi_references
                ):

                    score = similarity_score(m1, m2)

                    if score >= 0.5:

                        edge = set([m1, m2])

                        edge_tuple = tuple(sorted(edge))

                        if edge_tuple not in seen_edges:

                            local_edges.append((edge, score))

                            seen_edges.add(edge_tuple)

        all_results.append((sentence, local_edges))

    return all_results


def extract_pairs_from_edges(edges):

    pairs = []

    for edge, score in edges:

        edge_list = list(edge)

        if len(edge_list) == 2:

            pairs.append(
                (
                    edge_list[0],
                    edge_list[1],
                    score
                )
            )

    return pairs