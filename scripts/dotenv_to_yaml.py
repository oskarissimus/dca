#!python

from dotenv import dotenv_values

config = dotenv_values(".env")
with open(".env.yaml", "w", encoding="utf-8") as f:
    lines = [f'{k}: "{v}"' for k, v in config.items()]
    f.write("\n".join(lines))
