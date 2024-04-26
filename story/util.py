import re
import uuid
import json

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


def remove_before_first_numbered_dot(text):
    pattern = r"1\."
    match = re.search(pattern, text)
    if match:
        start_index = match.start()
        return text[start_index:]
    else:
        return text

def split_string_by_numbered_dots(text):  
  text = remove_before_first_numbered_dot(text)
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


def process_string_to_json(input_string):    
    pattern = r'(.*?)(\[.*?\])?\[(part[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|partLast)\]'
    match = re.search(pattern, input_string)

    if match:
        meta = match.group(2) if match.group(1) else ""
        value = match.group(1)
        uuid = match.group(3)[4:]  # Remove the '[part' and ']' from the UUID

        result = {
            "value": value,
            "uuid": uuid,
            "meta": meta,
            "error": ""
        }

        return json.dumps(result)
    else:
        return json.dumps({"error":"invalid"})

def save_to_file(file_name, value):
  value_to_save = process_string_to_json(value)
  with open(f"{file_name}.json", 'w') as file:
    file.write(value_to_save)

def id_next(actual_next_id = None):
  return (str(uuid.uuid4()), str(uuid.uuid4())) if actual_next_id is None else (actual_next_id, str(uuid.uuid4()))

def save_list_to_files(list_to_save):  
  this_id, next_id = id_next()
  origin_id = this_id
  last_this_id = this_id
  for s in list_to_save:    
    save_to_file(f"data/{this_id}", s + f"[part{next_id}]" if s != list_to_save[-1] else s + f"[partLast]")
    last_this_id = this_id
    this_id, next_id = id_next(next_id)
  print(f"last_this_id = {last_this_id}")
  return origin_id