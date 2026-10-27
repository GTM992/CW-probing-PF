grapheme_features = {
    # Vowels (by default voiced=0, soft=0, stressed=0 - stress will be determined by function)
    'а': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'о': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'у': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ы': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'э': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    # Vowels indicating palatalisation of a previous consonant
    'е': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ё': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'и': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ю': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'я': {'vowel': 1, 'voiced': 0, 'soft': 0, 'stressed': 0},

    # Consonants (voiced) paired by voiced
    'б': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'в': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'г': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'д': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'ж': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'з': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},

    # Consonants (unvoiced) paired by voiced
    'п': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ф': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'к': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'т': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ш': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'с': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},

    # Consonants (always voiced)
    'л': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'м': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'н': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'р': {'vowel': 0, 'voiced': 1, 'soft': 0, 'stressed': 0},
    'й': {'vowel': 0, 'voiced': 1, 'soft': 1, 'stressed': 0}, # й - always soft

    # Consonants (always unvoiced)
    'х': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ц': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0}, # ц - unpalatalizable
    'ч': {'vowel': 0, 'voiced': 0, 'soft': 1, 'stressed': 0}, # ч - always soft
    'щ': {'vowel': 0, 'voiced': 0, 'soft': 1, 'stressed': 0}, # щ - always soft

    # Знаки (не имеют самостоятельных признаков звука, но важны для контекста соседей)
    # Если они дойдут до записи в датасет, их можно отфильтровать или оставить с нулями
    'ь': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
    'ъ': {'vowel': 0, 'voiced': 0, 'soft': 0, 'stressed': 0},
}