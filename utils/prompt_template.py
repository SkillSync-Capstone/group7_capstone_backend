PROMPT_LIMIT = 3750

def build_prompt(query, context_chunks):
    prompt_start = (
        "Given the context below, provide a detailed explanation. If the context is empty or "
        "not related to the question, draw from general knowledge to respond. Include examples, "
        "discuss implications, and thoroughly explore the concept, focusing on how it works, "
        "its applications, and any significant limitations.\n"
    )
    
    prompt_end = f"\nQuestion: {query}\nAnswer:"
    
    if not context_chunks:  
        prompt_body = "\n[No context provided.]"
    else:
        prompt_body = ""
        current_length = len(prompt_start) + len(prompt_end) + 50  
        
        for chunk in context_chunks:
            chunk_with_separator = "\n" + chunk
            if current_length + len(chunk_with_separator) <= PROMPT_LIMIT:
                prompt_body += chunk_with_separator
                current_length += len(chunk_with_separator)
            else:
                break
    
    prompt = prompt_start + prompt_body + prompt_end
    return prompt
