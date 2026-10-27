import torch
from transformers import VitsModel, AutoTokenizer
import numpy as np

# Assumed shape of target features that are going to be predicted
from grapheme_dict import grapheme_features

# We'll be changing the aforementioned features based on phonetical patterns of Russian
import phonetical_functions

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Loading the model 
model_name = "utrobinmv/tts_ru_free_hf_vits_low_multispeaker"
model = VitsModel.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.eval()

# 2. Variable to intercept the tensor from the text encoder 
encoder_hidden_states = None

def hook_fn(module, input, output):
    global encoder_hidden_states
    encoder_hidden_states = output.last_hidden_state

# Registering a hook on a VITS Text Encoder
hook_handle = model.text_encoder.register_forward_hook(hook_fn)


# model accepts lowercase only
# All the texts will be stored there
russian_corpus = [
    """Ночью двадцать третьего июня начал извергаться самый высокий 
действующий вулкан в Евразии - Ключевской. Об этом сообщила руководитель 
Камчатской группы реагирования на вулканические извержения, ведущий 
научный сотрудник Института вулканологии и сейсмологии ДВО РАН Ольга Гирина.
«Зафиксированное ночью не просто свечение, а вершинное эксплозивное 
извержение стромболианского типа. Пока такое извержение никому не опасно: 
ни населению, ни авиации» пояснила ТАСС госпожа Гирина."""
]

# model vocabulary doesn't have uppercase symbols
for i, text in enumerate(russian_corpus):
    russian_corpus[i] = text.lower()


probing_dataset = []
special_ids = tokenizer.all_special_ids

# 3. Probing dataset consolidation:
for text in russian_corpus:
    # Converting letters to their vocabulary numeric equivalents
    inputs = tokenizer(text, return_tensors="pt").to(device)
    input_ids = inputs["input_ids"].squeeze(0)
    
    # Converting IDs back to chars. input_ids and raw_tokens have equal lengths
    raw_tokens = tokenizer.convert_ids_to_tokens(input_ids.tolist())
    
    print(f"\nОбработка текста: '{text}'")
    print(f"Токены из модели: {raw_tokens}")
    
    with torch.no_grad():
        # To retrieve the Text Encoder tensor, a forward pass through the whole model is required
        # This model needs speaker_id (0 or 1, male or female)
        outputs = model(**inputs, speaker_id=torch.tensor([0]).to(device))

        ###
        # waveform = outputs.waveform if hasattr(outputs, "waveform") else outputs[0]
        # Relaying to CPU, convertibg to NumPy and removing extra batch dimension
        #audio_data = waveform.squeeze().cpu().numpy()

        #scipy.io.wavfile.write("tts_audio1.wav", rate=model.config.sampling_rate, data=audio_data)
        ###

        # Retreiving the matrix (2 * T + 1, 192)
        encoder_embeddings = encoder_hidden_states.squeeze(0).cpu().numpy()
    
    mask = []
    for idx, t in enumerate(raw_tokens):
        clean_t = t.replace(" ", "").strip()
        
        # Проверяем, является ли токен системным (<s>, </s>, <pad>, <unk>)
        is_special = input_ids[idx].item() in special_ids
        
        # Условие исключения: пробелы, пунктуация, спец-токены и мета-знак ударения '+'
        if t.isspace() or clean_t in ['', '.', ',', '!', '?', '-', ';', '"', "'", "»", "«", '+'] or is_special:
            mask.append(False)
        else:
            mask.append(True)
    mask = np.array(mask)

    # removing all elements corresponding to punctuation and whitespaces (both technical and from the text)
    filtered_input_ids = input_ids[mask]
    filtered_tokens = [raw_tokens[idx] for idx, keep in enumerate(mask) if keep]
    filtered_embeddings = encoder_embeddings[mask]

    # A list with as many arguments as 3 lists before, required to pass the position of a token inside a text in a phonetical function 
    char_indices_in_original_text = [idx for idx, char in enumerate(text) if (not char.isspace() and not char in ['', '.', ',', '!', '?', '-', ';', '"', "'", "»", "«", '+'])]

    assert len(filtered_tokens) == len(char_indices_in_original_text), \
        f"Рассинхронизация! Токенов: {len(filtered_tokens)}, Индексов текста: {len(char_indices_in_original_text)}"
    
    # Assembling the probing dataset 
    for i, token_id in enumerate(filtered_input_ids.tolist()):
            
        token_str = filtered_tokens[i].replace(" ", "").strip()
   
        if token_str in grapheme_features:
            embedding = filtered_embeddings[i]  # Shape of (192,)
            features = grapheme_features[token_str].copy()
            original_text_pos = char_indices_in_original_text[i]

            # Section for adjusting features contextually
            if phonetical_functions.check_voiced(text, original_text_pos):
                features["voiced"] = 1
            if phonetical_functions.check_palatized(text, original_text_pos):
                features["soft"] = 1
            #

            probing_dataset.append({
                'phoneme': token_str,
                'embedding': embedding,
                'features': features
            })
            print(f"  Символ '{token_str}' (поз. в тексте: {original_text_pos}): извлечен вектор {embedding.shape} с таргетами {features}")

# Removing the hook
hook_handle.remove()
print(f"\nСбор завершен! Всего в датасете: {len(probing_dataset)} объектов.")

import torch
import os

output_filename = "probing_dataset.pt"

# Checking the length
if len(probing_dataset) > 0:
    print(f"\nСохранение датасета...")
    
    # Saving to disk
    torch.save(probing_dataset, output_filename)
    
    # Getting the file size
    file_size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"Датасет успешно сохранен в файл: '{output_filename}'")
    print(f"Всего объектов (фонем): {len(probing_dataset)}")
    print(f"Размер файла на диске: {file_size_mb:.2f} MB")
else:
    print("Ошибка: probing_dataset пуст, нечего сохранять!")