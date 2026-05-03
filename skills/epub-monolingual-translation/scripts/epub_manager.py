import zipfile
import os
import shutil

def extract_epub(input_file, temp_dir):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    print(f"Extracted {input_file} to {temp_dir}")

def pack_epub(temp_dir, output_file):
    # EPUB reconstruction rules:
    # 1. mimetype file must be first and uncompressed
    # 2. Other files can be compressed
    
    with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zip_ref:
        # Add mimetype first, uncompressed
        mimetype_path = os.path.join(temp_dir, 'mimetype')
        if os.path.exists(mimetype_path):
            zip_ref.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, temp_dir)
                
                if relative_path == 'mimetype':
                    continue
                
                zip_ref.write(full_path, relative_path)
    print(f"Packed {output_file} from {temp_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python epub_manager.py [extract|pack] [source] [target]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    src = sys.argv[2]
    tgt = sys.argv[3]
    
    if cmd == "extract":
        extract_epub(src, tgt)
    elif cmd == "pack":
        pack_epub(src, tgt)
