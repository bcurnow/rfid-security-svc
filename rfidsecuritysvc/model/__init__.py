class BaseModel:
  def to_json(self):
    return self.__dict__

  def __str__(self):
    return str(self.__dict__)

  def __repr__(self):
    return self.__str__()
