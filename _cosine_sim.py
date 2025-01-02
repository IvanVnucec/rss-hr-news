import math

def char_cosine_similarity(str1, str2):
    # Convert characters to their ASCII/Unicode values, assuming ASCII for simplicity
    vec1 = [ord(c) for c in str1]
    vec2 = [ord(c) for c in str2]
    
    # Pad the shorter vector with zeros to match length
    max_len = max(len(vec1), len(vec2))
    vec1 += [0] * (max_len - len(vec1))
    vec2 += [0] * (max_len - len(vec2))
    
    # Compute dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Compute magnitudes
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))
    
    # Avoid division by zero
    if mag1 == 0 or mag2 == 0:
        return 0
    
    # Cosine similarity
    return dot_product / (mag1 * mag2)

# Example usage
str1 = "policija"
str2 = "policijom"
similarity = char_cosine_similarity(str1, str2)
print(f"Normalized similarity score (cosine similarity): {similarity}")
