import os
import json
import re

def is_schema_or_code(text):
    if '\n' in text and ('{' in text or '}' in text or 'type ' in text or 'schema' in text or 'graphql' in text.lower()):
        return True
    return False

def safe_compress_text(text, is_parameter=False):
    if not isinstance(text, str):
        return text
    
    cleaned = re.sub(r'\s+', ' ', text).strip()
    if not cleaned:
        return cleaned
        
    if is_schema_or_code(text):
        return text.strip()
        
    if is_parameter:
        return cleaned
        
    temp = cleaned.replace("e.g.", "___EG___").replace("i.e.", "___IE___").replace("etc.", "___ETC___")
    sentences = re.split(r'\. |\? |! ', temp)
    first_sentence = sentences[0]
    
    first_sentence = first_sentence.replace("___EG___", "e.g.").replace("___IE___", "i.e.").replace("___ETC___", "etc.")
    
    if len(first_sentence) > 3 and not first_sentence.endswith(('.', '?', '!')):
        first_sentence += '.'
        
    if len(first_sentence) > 150:
        sub_parts = re.split(r', |; |: | - ', first_sentence)
        if len(sub_parts[0]) > 50:
            first_sentence = sub_parts[0]
            if not first_sentence.endswith('.'):
                first_sentence += '.'
                
    return first_sentence

def safe_compress_json_obj(obj, is_param=False):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == 'description' and isinstance(v, str):
                new_obj[k] = safe_compress_text(v, is_parameter=is_param)
            elif k == 'properties':
                new_obj[k] = safe_compress_json_obj(v, is_param=True)
            else:
                new_obj[k] = safe_compress_json_obj(v, is_param=is_param)
        return new_obj
    elif isinstance(obj, list):
        return [safe_compress_json_obj(item, is_param=is_param) for item in obj]
    else:
        return obj

def compress_instructions_md(content):
    lines = content.split('\n')
    compressed_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            compressed_lines.append('')
            continue
        if stripped.startswith('#') or stripped.startswith('-') or stripped.startswith('*'):
            compressed_lines.append(line)
        else:
            compressed_lines.append(safe_compress_text(line))
            
    result = '\n'.join(compressed_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip() + '\n'

def run_mcp_optimization(dry_run=True):
    mcp_dir = r"C:\Users\ajjuk\.gemini\antigravity\mcp"
    total_original_bytes = 0
    total_compressed_bytes = 0
    files_processed = []
    
    if not os.path.exists(mcp_dir):
        print("MCP directory does not exist")
        return
        
    for root, dirs, files in os.walk(mcp_dir):
        for file in files:
            path = os.path.join(root, file)
            size = os.path.getsize(path)
            total_original_bytes += size
            
            if file.endswith('.json'):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    compressed_data = safe_compress_json_obj(data)
                    comp_str = json.dumps(compressed_data, separators=(',', ':'))
                    new_size = len(comp_str.encode('utf-8'))
                    total_compressed_bytes += new_size
                    files_processed.append((path, size, new_size, 'json', compressed_data))
                    
                    if not dry_run:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(comp_str)
                except Exception as e:
                    print(f"Error processing JSON {path}: {e}")
                    total_compressed_bytes += size
                    
            elif file == 'instructions.md':
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    compressed_content = compress_instructions_md(content)
                    new_size = len(compressed_content.encode('utf-8'))
                    total_compressed_bytes += new_size
                    files_processed.append((path, size, new_size, 'md', compressed_content))
                    
                    if not dry_run:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(compressed_content)
                except Exception as e:
                    print(f"Error processing MD {path}: {e}")
                    total_compressed_bytes += size
            else:
                total_compressed_bytes += size
                
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTION'}")
    print(f"Total files processed: {len(files_processed)}")
    print(f"Total original size: {total_original_bytes} bytes")
    print(f"Total compressed size: {total_compressed_bytes} bytes")
    print(f"Reduction: {(total_original_bytes - total_compressed_bytes) / total_original_bytes * 100:.2f}%")
    print(f"Saved: {total_original_bytes - total_compressed_bytes} bytes")

if __name__ == '__main__':
    import sys
    dry = True
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        dry = False
    run_mcp_optimization(dry_run=dry)
