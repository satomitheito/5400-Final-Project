import transformers
import torch
import pandas as pd
import logging
logger = logging.getLogger(__name__)

encoder_model_name = "cl-tohoku/bert-base-japanese-v2"
decoder_model_name = "openai-community/gpt2"
src_tokenizer = transformers.BertJapaneseTokenizer.from_pretrained(encoder_model_name)
trg_tokenizer = transformers.PreTrainedTokenizerFast.from_pretrained(decoder_model_name)
model = transformers.EncoderDecoderModel.from_pretrained("sappho192/jesc-ja-en-translator")


def translate_in_chunks(text, max_length=512):
    # Tokenize the text into tokens without truncating
    tokens = src_tokenizer(text, return_tensors='pt', truncation=False)['input_ids'][0]
    # Split tokens into chunks that fit the max input length
    chunks = tokens.split(max_length - 2)  # Reserve space for special tokens
    translations = []

    for chunk in chunks:
        chunk = chunk.unsqueeze(0)  # Add batch dimension
        embeddings = {'input_ids': chunk}
        try:
            output = model.generate(
                **embeddings,
                max_length=max_length,
                no_repeat_ngram_size=2
            )
            translations.append(trg_tokenizer.decode(output[0], skip_special_tokens=True))
        except Exception as e:
            print(f"Error translating chunk: {e}")
            translations.append("")

    return " ".join(translations)  # Combine all chunk translations

def translate_articles(df):
    translations = []
    counter = 1
    for content in df['content']:
        try:
            logger.info("Translating article " + str(counter))
            translation = translate_in_chunks(content)  # Use the new chunking function
            translations.append(translation)
            logger.info("Translation for article " + str(counter) + " complete")
            counter += 1
        except Exception as e:
            translations.append(None)
            logger.info(f"Error translating content: {e}")
    
    df['translation'] = translations
    return df
