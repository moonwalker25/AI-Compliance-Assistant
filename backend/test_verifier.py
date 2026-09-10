from services.mapping_verifier import verify_mapping

result = verify_mapping(
    country="India",
    industry="Healthcare",
    suggested_act="FACTORIES ACT",
    available_acts=[
        "FACTORIES ACT",
        "GST ACT",
        "COMPANIES ACT",
        "DPDP ACT"
    ]
)

print("\nVerification Result:")
print(result)