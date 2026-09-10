from services.mapping_service import get_mapping
from services.mapping_verifier import verify_mapping
from services.suggestion_service import save_suggestion
from services.retrieval_engine import get_all_acts

def check_act_applicability(
    country,
    industry,
    act_name,
    db
):

    # ------------------------------------------
    # 1. CHECK APPROVED / EXISTING MAPPING
    # ------------------------------------------

    mapped_acts = get_mapping(
        country,
        industry,
        db
    )

    for act in mapped_acts:

        if act.strip().lower() == act_name.strip().lower():

            return {
                "status": "APPLICABLE",
                "applicable": True,
                "act": act,
                "reason": (
                    f"{act} is already mapped as applicable "
                    f"to the {industry} industry in {country}."
                )
            }


    # ------------------------------------------
    # 2. CHECK IF ACT EXISTS IN COUNTRY DATABASE
    # ------------------------------------------

    available_acts = get_all_acts(
        country,
        db
    )

    matched_act = None

    for act in available_acts:

        if act.strip().lower() == act_name.strip().lower():

            matched_act = act
            break


    if not matched_act:

        return {
            "status": "NOT_FOUND",
            "applicable": False,
            "act": act_name,
            "reason": (
                f"I couldn't find {act_name} in the "
                f"available compliance database for {country}."
            )
        }


    # ------------------------------------------
    # 3. AI VERIFICATION
    # ------------------------------------------

    verification = verify_mapping(
        country,
        industry,
        matched_act,
        available_acts
    )


    # ------------------------------------------
    # 4. NOT APPLICABLE
    # ------------------------------------------

    if not verification.get("applicable"):

        return {
            "status": "NOT_APPLICABLE",
            "applicable": False,
            "act": matched_act,
            "reason": verification.get(
                "reason",
                "The Act does not currently appear applicable."
            ),
            "confidence": verification.get(
                "confidence",
                0
            )
        }


    # ------------------------------------------
    # 5. SAVE AS PENDING ADMIN REVIEW
    # ------------------------------------------

    suggestion = save_suggestion(
        country,
        industry,
        matched_act,
        verification,
        db
    )


    return {
        "status": suggestion.status,
        "applicable": None,
        "act": matched_act,
        "reason": verification.get("reason"),
        "confidence": verification.get("confidence")
    }