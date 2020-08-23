def min_length(min_len: int, field_name: str = "this", nullable=True):
    def _min_length(value):
        if nullable and value is None:
            return True, value
        if value and len(value) >= min_len:
            return True, value
        return False, f"Length of {field_name} field must at least {min_len} characters"

    return _min_length
