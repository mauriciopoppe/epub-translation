import sys
import os
from bs4 import BeautifulSoup, NavigableString

# Tags that typically contain human-readable text
TEXT_CONTAINERS = ['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'title', 'b', 'i', 'em', 'strong', 'td', 'th', 'div', 'section', 'header', 'footer']

def get_text_nodes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    
    nodes = []
    # Find all strings in the document
    for text in soup.find_all(string=True):
        if text.parent.name in ['script', 'style']:
            continue
        if not text.strip():
            continue
        nodes.append(text)
    return nodes, soup

def extract_text(file_path):
    nodes, _ = get_text_nodes(file_path)
    for i, node in enumerate(nodes):
        # Escape newlines for ID:N format
        clean_text = node.string.replace('\n', '\\n')
        print(f"ID:{i}|{clean_text}")

def apply_translations(file_path, translations_file, output_path):
    trans_map = {}
    with open(translations_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                parts = line.split('|', 1)
                if parts[0].startswith('ID:'):
                    id_val = int(parts[0][3:])
                    # Unescape newlines
                    text_val = parts[1].strip().replace('\\n', '\n')
                    trans_map[id_val] = text_val

    nodes, soup = get_text_nodes(file_path)
    for i, node in enumerate(nodes):
        if i in trans_map:
            node.replace_with(trans_map[i])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Applied translations to {output_path}")

def update_metadata(opf_path, target_lang_code):
    with open(opf_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    
    # Try multiple common namespaces/formats for language
    lang_tag = soup.find('dc:language') or soup.find('language')
    if lang_tag:
        lang_tag.string = target_lang_code
    
    with open(opf_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Updated metadata language to {target_lang_code}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python translate_processor.py extract [file]")
        print("  python translate_processor.py apply [file] [translations_file] [output_file]")
        print("  python translate_processor.py metadata [opf_file] [lang_code]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "extract":
        extract_text(sys.argv[2])
    elif cmd == "apply":
        apply_translations(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "metadata":
        update_metadata(sys.argv[2], sys.argv[3])
