VOWELS = set("аоуэыиеёюя")
VOICED_PAIRED = set("бвгджз")
VOICELESS_PAIRED = set("пфктшс")
ALWAYS_SOFT = set("йчщ")
ALWAYS_HARD = set("жшц")
VOWELS_SOFTENERS = set("еёиюяь") # Vowels that palatalise the previous consonant, и 'Ь'

def get_clean_char_and_context(text: str, index: int):
    """Auxiliary function to retreive the next char"""
    char = text[index].lower()
    next_index = index + 1
    if next_index < len(text) and text[next_index] == '+':
        next_index+=1

    if next_index < len(text):
        next_char = text[next_index].lower()
    else: 
        next_char = ""
    return char, next_char

def check_voiced(text: str, index: int) -> int:
    char, next_char = get_clean_char_and_context(text, index)
    
    # If 'voiced' feature can not be changed for a letter
    if char not in VOICED_PAIRED and char not in VOICELESS_PAIRED:
        return 0 
        
    # Initial state from grapheme_features
    is_voiced = 1 if char in VOICED_PAIRED else 0
    
    # Rule 1: becoming 'unvoiced' on the end of a word (Before whitespace or punctuation)
    if char in VOICED_PAIRED and (next_char == "" or next_char in " .,!?:;"):
        return 0
        
    # Rule 2: Regressive assimilation by 'voiced' (before unvoiced consonant becomes unvoiced, and the opposite)
    if char in VOICED_PAIRED and next_char in VOICELESS_PAIRED:
        return 0
    if char in VOICELESS_PAIRED and next_char in VOICED_PAIRED and next_char != 'в':
        return 1
        
    return is_voiced

def check_palatized(text: str, index: int) -> int:
    char, next_char = get_clean_char_and_context(text, index)
    if char in VOWELS: return 0
    if char in ALWAYS_SOFT: return 1
    if char in ALWAYS_HARD: return 0
    
    # If the letter following after the consonant is a softener, then the current sound is palatalized
    if next_char in VOWELS_SOFTENERS:
        return 1
        
    return 0



def check_stressed(text: str, index: int) -> int:
    """
    Определяет, является ли гласная буква под указанным индексом ударной.
    Возвращает 1, если ударная, и 0, если безударная (или если это согласная).
    """
    char = text[index].lower()
    
    # 1. No stress for consonants
    if char not in VOWELS:
        return 0
        
    # 2. ё is syressed by default
    if char == 'ё':
        return 1
        
    # 3. Looking forward
    # Если за текущей гласной идет знак '+', значит она ударная
    next_index = index + 1
    if next_index < len(text):
        if text[next_index] == '+' and text[next_index+1] in VOWELS:
            return 1

    # Во всех остальных случаях гласная считается безударной (редуцированной)
    return 0
