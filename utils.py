import re

def sanitize_mermaid(code: str) -> str:
    """
    Cleans Mermaid code to prevent syntax errors.
    """

    code = re.sub(r'^mermaid\s+', '', code, flags=re.IGNORECASE).strip()

    def quote_labels(match):
        node_id = match.group(1)
        bracket_type = match.group(2)
        content=match.group(3)
        end_bracket = match.group(4)

        if content.startswith('"') and content.endswith('"'):
            return f"{node_id}{bracket_type}{content}{end_bracket}"
        
        return f'{node_id}{bracket_type}"{content}"{end_bracket}'
    
    code = re.sub(r'(\w+)(\[|\(|\{)(.*?)(\]|\)|\})', quote_labels, code)

    return code