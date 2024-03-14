from typing import List
import re


def split_text(text: str, *chunks: int) -> List[str]:
    result = []
    current_chunk, chunk_index = '', 0
    for sentence in re.findall(r'.{1,%d}(?:\s+|$)' % chunks[chunk_index], text):
        if len(current_chunk) + len(sentence) <= chunks[chunk_index]:
            current_chunk += sentence
        else:
            result.append(current_chunk)
            current_chunk = sentence
            chunk_index = min(chunk_index + 1, len(chunks) - 1)
    if current_chunk:
        result.append(''.join(current_chunk))
    return result