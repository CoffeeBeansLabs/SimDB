class DefaultResultMapper:
  def __init__(self, config):
    config.

  def map(self, content, fields=[]):
    result = {
      "id": content.get("id"),
      "rank": content.get("rank")
    }
    for field in fields:
      result[field] = content.get(field)

    return result
