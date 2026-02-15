import re

def sanitize_mermaid(code: str) -> str:
    """
    Cleans Mermaid code to prevent syntax errors and common LLM-generated bugs.
    """
    if not code:
        return ""
    code = re.sub(r'^mermaid\s+', '', code, flags=re.IGNORECASE).strip()

    # 2. Fix invalid arrow syntax like -->|> or --|Label|>
    # Mermaid expects: A --> B  OR  A -->|Label| B
    code = re.sub(r'--+>+>', '-->', code) 
    code = re.sub(r'\|(.*?)\|>', r'|"\1"|', code) # Fixes the |Label|> issue by quoting and removing '>'

    # 3. Robust label quoting for nodes (A["Label"])
    def quote_labels(match):
        node_id = match.group(1)
        bracket_open = match.group(2)
        content = match.group(3).strip()
        bracket_close = match.group(4)

        # Remove existing quotes to prevent nesting and strip special chars
        clean_content = content.replace('"', '').replace('(', '').replace(')', '').strip()
        
        return f'{node_id}["{clean_content}"]'
    
    # Regex to find nodes with any bracket type: [], (), {}
    code = re.sub(r'(\w+)(\[|\(|\{)(.*?)(\]|\)|\})', quote_labels, code)

    # Characters like & or / can break the parser if not inside quotes
    lines = []
    for line in code.split('\n'):
        if "-->" in line or "-.->" in line:
            # Clean labels on arrows if they exist
            line = re.sub(r'\|(.*?)\|', lambda m: f'|"{m.group(1).replace("&", "and")}"|', line)
        lines.append(line)

    return "\n".join(lines)