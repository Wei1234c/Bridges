db_path = 'C:\\Users\\Wei\\Dropbox\\Coding\\notebooks\\專案\\已完成\\Bridges\\bitbucket\\github\\codes\\bridges\\universal_serial_bus\\spec\\db\\usb_2_0.sqlite'
db_url = 'sqlite:///' + db_path

from bridges.universal_serial_bus.orm import ModelBuilder


# ModelBuilder.gen_all(db_url)

tables = ModelBuilder.get_tables(db_url)
for t in tables:
    if t.name == 'class_code':
        for c in t.columns:
            if c.name == 'base_code':
                print(type(c))
                print(type(c.type))
                print(c.type.length)
