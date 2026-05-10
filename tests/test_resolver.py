from marathi_coref import resolve_coreference

def test_coreference():

    sentences = [
        "राम शाळेत जातो. तो हुशार आहे."
    ]

    result = resolve_coreference(sentences)

    assert len(result) > 0