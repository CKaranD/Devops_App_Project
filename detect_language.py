import cld3

def detect_language(user_input):
    lang_id = cld3.get_language(user_input)

    if lang_id.language == 'zh-Latn' or lang_id.language == 'zh':
        language = "Chinese"
    elif lang_id.language == 'id' or lang_id.language == 'ms':
        language = "Bahasa Melayu"    
    else:
        language = "English"

    return language