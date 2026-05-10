from marathi_coref import resolve_coreference

sentences = [

    "सारिकाने जेवण बनवले, तिने चांगले जेवण बनवले.",

    "मित्रांनी भेट घेतली, त्यांनी खूप मजा केली.",

    "राम शाळेत जातो तो हुशार आहे",

    "मित्रांनी सहल आखली. त्यांनी खूप मजा केली",
]

results = resolve_coreference(sentences)

print("\n🧠 Marathi Coreference Resolution\n")

for idx, (sentence, edges) in enumerate(results, 1):

    print("=" * 60)

    print(f"\n📌 Sentence {idx}:")
    print(sentence)

    print("\n🔗 Hyperedges:\n")

    if not edges:
        print("No hyperedges found.")

    else:

        for edge, score in edges:

            edge_text = ", ".join(edge)

            print(
                f"   ➤ [{edge_text}]  ---> Score: {score}"
            )

    print()