from schema import Schema

conf_schema_users = Schema(
    {
        "name": str,
        "email": str,
        "age": int
    }
)
