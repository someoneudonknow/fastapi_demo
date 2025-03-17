import re


def replace_template_data(template_string: str, data: dict) -> str:
    for key, value in data.items():
        regex = re.compile(r"\{\{" + re.escape(key) + r"\}\}")
        template_string = regex.sub(str(value), template_string)

    return template_string
