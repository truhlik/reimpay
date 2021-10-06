from constance import config


def get_vat_rate_int() -> int:
    return config.VAT_RATE


def get_vat_rate_float() -> float:
    return 1 + (get_vat_rate_int() / 100)
