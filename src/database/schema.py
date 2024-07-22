from typing import List
from bson import json_util
import json

def SchemaOutput(item) -> dict:
    doc = json_util.dumps(item)
    return json.loads(doc)