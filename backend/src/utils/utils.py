import re

def sanitize_mermaid(code: str) -> str:
    """
    Cleans Mermaid code to prevent syntax errors.
    """

    code = re.sub(r'^mermaid\s+', '', code, flags=re.IGNORECASE).strip()

    def quote_labels(match):
        node_id = match.group(1)
        bracket_type = match.group(2)
        content=match.group(3).strip()
        end_bracket = match.group(4)

        clean_content = content.replace('"', '').strip()
        
        return f'{node_id}{bracket_type}"{clean_content}"{end_bracket}'
    
    code = re.sub(r'(\w+)(\[|\(|\{)(.*?)(\]|\)|\})', quote_labels, code)

    return code