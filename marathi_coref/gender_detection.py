import unicodedata

def guess_gender(word_text):

    word = unicodedata.normalize(
        'NFC',
        word_text.strip()
    )

    male_suffixes = [
        'अ', 'य', 'श', 'न',
        'ध', 'ल', 'नंद',
        'उ', 'ऊ', 'त',
        'र', 'ष्णु', 'षि',
        'जी', 'ती'
    ]

    female_suffixes = [
        'इ', 'ई', 'आ',
        'ा', 'ी', 'धि',
        'नी', 'का', 'नी'
    ]

    if any(word.endswith(suffix) for suffix in male_suffixes):
        return "male"

    elif any(word.endswith(suffix) for suffix in female_suffixes):
        return "female"

    return "neutral"