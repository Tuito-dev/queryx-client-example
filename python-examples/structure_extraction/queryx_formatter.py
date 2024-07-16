import os
import sys

from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.schema import CreateTable

class QueryXFormatter:

    SUPPORTED_TYPES = {
        "sqlite": "sqlite:///",
        "mysql": "mysql+mysqldb://root:@localhost/",
        "pg": "postgresql://postgres:@localhost/",
    }

    def __init__(self, db_file_name: str):

        name_elements = os.path.basename(db_file_name).split(".")
        if len(name_elements) < 2:
            raise ValueError(f"Cannot retrieve database type from {db_file_name}")

        self._name = name_elements[0]
        self._type = name_elements[1]
        if self._type not in QueryXFormatter.SUPPORTED_TYPES.keys():
            raise ValueError(f"Unsupported database type: {self._type }\nSupported database types are: {QueryXFormatter.SUPPORTED_TYPES.keys()}")

        db_uri = QueryXFormatter.SUPPORTED_TYPES[self._type] + db_file_name
        self._engine = create_engine(db_uri, echo=False)
        self._inspector = inspect(self._engine)

    def get_ddl(self) -> list:

        metadata = MetaData()
        metadata.reflect(bind=self._engine)

        ddl_list = []
        for table in metadata.tables.values():
            ddl = str(CreateTable(table).compile(self._engine)).strip()
            ddl_list.append(ddl)
        return ddl_list

    def build_schema(self) -> dict:

        metadata = MetaData()
        metadata.reflect(bind=self._engine)

        schema_dict = {
            "tables": [],
            "businessRules": [],
            "dbName": self._name,
            "dbType": self._type,
        }

        for table_name in self._inspector.get_table_names():
            columns = self._inspector.get_columns(table_name)
            table_info = {
                "table_name": table_name,
                "description": "",
                "primary_keys": [column["name"] for column in columns if column["primary_key"]],
                "constraints": [
                    {
                        "column": fk["constrained_columns"][0],
                        "join_column": fk["referred_columns"][0],
                        "join_table": fk["referred_table"],
                    }
                    for fk in self._inspector.get_foreign_keys(table_name)
                ],
                "columns": [
                    {
                        "name": column["name"],
                        "type": column["type"].__visit_name__,
                        "nullable": column["nullable"],
                        "description": "",
                        "labels": "",
                        "values": [],
                    }
                    for column in columns
                ],
            }
            schema_dict["tables"].append(table_info)

        return schema_dict

if __name__ == "__main__":

    import json

    print()
    print("*** QueryX database schema formatter ***\n")

    if len(sys.argv) < 2:
        print(f"  usage: python {sys.argv[0]} <db-file> [<business-rules-file>]\n")
        sys.exit(1)

    db_file = sys.argv[1]
    db_formatter = QueryXFormatter(db_file)
    db_schema = db_formatter.build_schema()
    db_schema_file = db_file.replace("." + db_file.split(".")[-1], ".json")

    if len(sys.argv) > 2:
        br_file = sys.argv[2]
        with open(br_file, 'r', encoding='utf-8') as text_file:
            db_schema["businessRules"] = text_file.readlines()
        for br in db_schema["businessRules"]:
            br = br.strip()

    if len(db_schema["businessRules"]) == 0:
        print("  * from", db_file)
    else:
        print("  * from", db_file, "and", br_file)
    #print("  * schema =", json.dumps(db_schema, indent=4))
    print("  * save into", db_schema_file)
    with open(db_schema_file, 'w', encoding='utf-8') as json_file:
        json.dump(db_schema, json_file, indent=2)
    print("  * table & columns descriptions, labels, values can be added manually")
    if len(db_schema["businessRules"]) == 0:
        print("    as well as business rules")
    print()
