class BaseModel:
    def to_json(self):
        return self.__dict__.copy()


    def _read_only_keys(self):
        """
        Identifies any keys on this object that are defined read only at the API tier.
        Subclasses should override to specify their keys.
        """
        return []

    
    def to_json_rw(self):
        """ Returns a JSON compatible value stripped of keys which are defined read only at the API."""
        copy = self.__dict__.copy()
        for key in self._read_only_keys():
            del copy[key]

        return copy


    def __str__(self):
        return str(self.__dict__)


    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)
