PROMPT_LIMIT = 3750

def build_prompt(query, context_chunks):
    prompt_start = (
        "Given the context below, please provide a detailed explanation. "
        "If the information is not found in the context, respond with 'I don't know'. "
        "Otherwise, include examples, discuss the implications, and explore the concept thoroughly. "
        "If possible, address the following in your response: how it works, its applications, "
        "and any significant limitations.\n"
    )
    
    prompt_end = f"\nQuestion: {query}\nAnswer:"
    
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
