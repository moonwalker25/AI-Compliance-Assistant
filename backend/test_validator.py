from services.response_validator import validate_response

class DummyRecord:
    regulation = "Clinical Establishments Act"
    
record = DummyRecord()

print("========== Test 1 ==========")
print(validate_response("", record))


print("\n========== Test 2 ==========")
print(validate_response("     ", record))


print("\n========== Test 3 ==========")
print(validate_response("Yes.", record))


print("\n========== Test 4 ==========")
print(validate_response(
    """
    The Clinical Establishments Act requires healthcare facilities
    to register with the appropriate authority before operating.
    """,
    record
))


print("\n========== Test 5 ==========")
print(validate_response(
    """
    Hospitals must register with the government before operating.
    """,
    record
))

    