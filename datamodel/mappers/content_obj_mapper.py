import copy


class ContentMapper:
  def __init__(self, config):
    self.config = config

  def map(self, dto):
    fields_map = self.config.content_mapper_std_fields_map()
    content_vector = {
      "id": dto.get(fields_map["id"]),
      "vector": dto.get(fields_map["vector"]),
    }

    std_excluded = self.config.content_mapper_std_fields_excluded()
    if "content" not in std_excluded:
      content_vector["content"] = dto.get(fields_map.get("content", "content"))

    if "title" not in std_excluded:
      content_vector["title"] = dto.get(fields_map.get("title", "title"))

    std_fields = ["id", "vector", "content", "title"]

    if self.config.content_mapper_select_fields() != "*":
      select = self.config.content_mapper_select_fields()
      for key in select:
        content_vector[key] = dto.get(key)
      return content_vector

    exclude_fields = self.config.content_mapper_exclude_fields()

    ignore = std_fields + exclude_fields

    for key in dto.keys():
      if key in ignore:
        continue
      content_vector[key] = dto.get(key)

    return content_vector

  def from_content_dtos(self, dto_list):
    dtos = [self.map(dto) for dto in dto_list]
    return dtos

  @staticmethod
  def to_result_dto(content_vector, rank, only_ids=False):
    result = {}
    if not only_ids:
      result = copy.deepcopy(content_vector)
      result["rank"] = rank
      return result

    result["id"] = content_vector.get("id"),
    result["seq_id"] = content_vector.get("seq_id"),
    result["rank"] = rank,
    result["other_data"] = copy.deepcopy(content_vector.get("other_data"))
    return result
