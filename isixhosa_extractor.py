import PyPDF2
import re
from collections import defaultdict
import os

def is_likely_isixhosa(text):
    click_sounds = ['q', 'x', 'c']
    prefixes = ['um', 'aba', 'imi', 'izi', 'ama', 'isi', 'ulu','uku','ubu',]
    
    text = text.lower()
    words = text.split()
    
    if any(click in text for click in click_sounds):
        return True
    if any(word.startswith(prefix) for prefix in prefixes for word in words):
        return True
    
    return False

def extract_from_pdf(file_path):
    text_by_page = {}
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_by_page[page_num] = text
                else:
                    print(f"Warning: No text found on page {page_num}")
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None
    return text_by_page

def extract_from_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return {1: file.read()}  # Treat entire text file as one page
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None

def process_text(text, page_num, word_dict, phrase_dict, sentence_dict):
    # Extract words
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        if is_likely_isixhosa(word):
            word_dict[word.lower()]['pages'].add(page_num)
    
    # Extract phrases (2-5 words)
    phrases = re.findall(r'\b(?:\w+\s+){1,4}\w+\b', text)
    for phrase in phrases:
        if is_likely_isixhosa(phrase):
            phrase_dict[phrase.lower()]['pages'].add(page_num)
    
    # Extract sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        if is_likely_isixhosa(sentence):
            sentence_dict[sentence.strip()]['pages'].add(page_num)

def extract_isixhosa_content(file_path, output_path):
    word_dict = defaultdict(lambda: {'pages': set()})
    phrase_dict = defaultdict(lambda: {'pages': set()})
    sentence_dict = defaultdict(lambda: {'pages': set()})

    file_path = os.path.normpath(file_path)
    output_path = os.path.normpath(output_path)
    
    if not os.path.exists(file_path):
        return f"Error: The file {file_path} does not exist."
    
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.pdf':
        text_by_page = extract_from_pdf(file_path)
    elif file_extension.lower() in ['.txt', '.text']:
        text_by_page = extract_from_text(file_path)
    else:
        return f"Unsupported file type: {file_extension}"

    if text_by_page is None:
        return "Failed to extract text from the file."

    for page_num, text in text_by_page.items():
        process_text(text, page_num, word_dict, phrase_dict, sentence_dict)

    # Generate the formatted output
    output = f"isiXhosa content extracted from {os.path.basename(file_path)}:\n\n"
    
    output += "WORDS:\n"
    for i, (word, info) in enumerate(sorted(word_dict.items()), 1):
        pages = ', '.join(map(str, sorted(info['pages'])))
        output += f"{i}. **{word}** [Pages: {pages}]\n"
    
    output += "\nPHRASES:\n"
    for i, (phrase, info) in enumerate(sorted(phrase_dict.items()), 1):
        pages = ', '.join(map(str, sorted(info['pages'])))
        output += f"{i}. **{phrase}** [Pages: {pages}]\n"
    
    output += "\nSENTENCES:\n"
    for i, (sentence, info) in enumerate(sorted(sentence_dict.items()), 1):
        pages = ', '.join(map(str, sorted(info['pages'])))
        output += f"{i}. {sentence} [Pages: {pages}]\n"

    # Write output to file
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(output)
    except Exception as e:
        return f"Error writing to output file: {e}"

    return f"Extraction complete. Output saved to {output_path}"

# Usage
input_file = r"file_path"  # text or .pdf
output_file = r"output_path"
result = extract_isixhosa_content(input_file, output_file)
print(result)