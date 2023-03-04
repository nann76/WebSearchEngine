
# 定义IDMAP，实现id和str的转换
class IdMap:
    """Helper class to store a mapping from strings to ids."""
    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        """Return number of terms stored in the IdMap"""
        return len(self.id_to_str)

    def _get_str(self, i):
        """Returns the string corresponding to a given id (`i`)."""
        ### Begin your code
        return self.id_to_str[i]
        ### End your code

    def _get_id(self, s):
        """Returns the id corresponding to a string (`s`).
        If `s` is not in the IdMap yet, then assigns a new id and returns the new id.
        """
        ### Begin your code
        if s not in self.str_to_id:
            self.id_to_str.append(s)
            temp =self.id_to_str.index(s)
            self.str_to_id[s ] =temp
            # 返回新分配的id
            return temp

        # 如果s在，返回已存在的id
        return self.str_to_id[s]
        ### End your code

    def __getitem__(self, key):
        """If `key` is a integer, use _get_str;
           If `key` is a string, use _get_id;"""
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError