import re
import uuid

def split_text_by_block(text):
  pattern = r"Блок\s+\d+."  
  blocks = re.split(pattern, text)
  blocks = [block.strip() for block in blocks if block.strip()]

  return blocks


def extract_number(string):
    match = re.search(r'[-+]?\d*\.?\d+', string)
    if match:
        return float(match.group())
    return None


def split_string_by_numbered_dots(text):
  pattern = r"\d+\."
  sublists = re.split(pattern, text)
  sublists = [sublist.strip() for sublist in sublists if sublist.strip()]
  return sublists


def add_meta(base, meta):
  for idx in range(len(base)):
    key = str(idx)
    if key in meta:
      base[idx] = base[idx] + meta[key]
  return base


def save_to_file(file_name, value):
  with open(file_name, 'w') as file:
    file.write(value)

def id_next(actual_next_id = None):
  return (str(uuid.uuid4()), str(uuid.uuid4())) if actual_next_id is None else (actual_next_id, str(uuid.uuid4()))

def save_list_to_files(list_to_save):  
  this_id, next_id = id_next()
  for s in list_to_save:
    print(s, f"[part{next_id}]")
    save_to_file(f"data/{this_id}", s + f"[part{next_id}]")
    this_id, next_id = id_next(next_id)