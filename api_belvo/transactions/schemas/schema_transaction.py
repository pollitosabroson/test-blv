from schema import Schema

conf_schema_transaction = Schema(
    {
        "reference": str,
        "account": str,
        "date": str,
        "amount": str,
        "type": str,
        "category": str,
        "user_id": str,
    }
)

conf_schema_transaction_sumary = Schema(
    {
        "account": str,
        "balance": str,
        "total_inflow": str,
        "total_outflow": str
    }
)

conf_schema_transaction_category = Schema(
    {
        "inflow": dict,
        "outflow": dict
    }
)
