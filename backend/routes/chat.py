from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.chat import ChatRequest
from database.database import get_db

from services.context_resolver import resolve_context

from services.conversation_state import (
    get_state,
    update_state,
    clear_state
)

from services.retrieval_engine import (
    get_all_acts,
    get_particulars,
    get_description
)

from services.industry_reasoner import find_applicable_acts

from services.mapping_service import (
    save_mapping,
    get_mapping
)

from services.mapping_verifier import verify_mapping

from services.suggestion_service import save_suggestion
from services.suggestion_detector import detect_suggestion

from services.conversation_router import route_message

from services.conversation_service import (
    answer_follow_up,
    clean_llm_formatting,
    generate_conversation_title
)

from services.conversation_storage import (
    create_conversation,
    get_conversation,
    save_message
)

from services.industry_service import (
    get_industries_by_country
)

from services.applicability_service import (
    check_act_applicability
)

from models.conversation import ConversationMessage
from services.llm_service import ask_llm

router = APIRouter()


# ============================================================
# DATABASE CONVERSATION HISTORY
# ============================================================

def get_database_history(
    session_id,
    db,
    limit=50
):
    """
    Load persistent conversation history from SQLite.
    """

    messages = (
        db.query(ConversationMessage)
        .filter(
            ConversationMessage.conversation_id == session_id
        )
        .order_by(
            ConversationMessage.created_at.asc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "role": message.sender,
            "content": message.message
        }
        for message in messages
    ]


# ============================================================
# SAVE COMPLETE EXCHANGE
# ============================================================

def persist_exchange(
    session_id,
    user_message,
    assistant_message,
    db,
    assistant_data=None
):
    """
    Persist both sides of a conversation exchange.
    """

    # Save user message
    save_message(
        session_id,
        "user",
        user_message,
        db
    )

    # Save assistant message + optional UI data
    save_message(
        session_id,
        "assistant",
        assistant_message,
        db,
        assistant_data
    )

# ============================================================
# CHAT ENDPOINT
# ============================================================

@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    session_id = request.session_id

    print("\n==============================")
    print("SESSION ID:", session_id)
    print("==============================")

    # ========================================================
    # GET / CREATE CONVERSATION
    # ========================================================

    conversation = get_conversation(
        session_id,
        db
    )

    if not conversation:

        try:

            title = generate_conversation_title(
                request.message
            )

            if not title:
                title = "New Conversation"

        except Exception as e:

            print(
                "Conversation title generation failed:",
                e
            )

            title = "New Conversation"

        create_conversation(
            session_id,
            db,
            title
        )

    # ========================================================
    # LOAD PERSISTENT HISTORY
    # ========================================================

    history = get_database_history(
        session_id,
        db
    )

    # ========================================================
    # LOAD CURRENT STATE
    # ========================================================

    state = get_state(
        session_id
    )

    print("\nConversation History:")
    print(history)

    print("\nCurrent Conversation State:")
    print(state)

    # ========================================================
    # ROUTE USER MESSAGE
    # ========================================================

    route = route_message(
        request.message,
        history,
        state
    )

    print("\nConversation Router:")
    print(route)

    intent = route.get(
        "intent",
        "OUT_OF_SCOPE"
    )

    print("Detected Intent:", intent)

    # ========================================================
    # ACKNOWLEDGEMENT
    # ========================================================

    if intent == "ACKNOWLEDGEMENT":

        answer = (
            "You're welcome! 😊 "
            "Feel free to ask if you'd like to explore anything else."
        )

        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )

        return {
            "message": answer
        }

    # ========================================================
    # GREETING
    # ========================================================

    if intent == "GREETING":

        answer = (
            "Hello! 👋 I'm your Enterprise AI Compliance Assistant. "
            "I can help you explore workplace compliance requirements "
            "across countries and industries. "
            "What would you like to know?"
        )

        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )

        return {
            "message": answer
        }
    
    # ========================================================
    # GENERAL COMPLIANCE QUESTION
    # ========================================================

    if intent == "GENERAL_COMPLIANCE_QUESTION":

        general_system_prompt = """
You are ComplianceAI, an Enterprise AI Compliance Assistant.

Answer the user's general question about compliance clearly,
accurately, and conversationally.

The user is asking for general educational information about
compliance or workplace compliance.

Do NOT assume a country, industry, Act, regulation, or compliance
requirement unless the user explicitly mentions one.

Do NOT use previous conversation context to force the answer toward
a specific Act or country.

Explain the concept in a simple and helpful way.

Do not automatically list specific Acts or regulations unless they
are genuinely necessary to answer the user's question.

OUTPUT FORMAT RULES:

- Use clean Markdown only.
- Use short paragraphs.
- Use headings only when useful.
- Use normal bullet points or numbered lists when appropriate.
- NEVER use Markdown tables.
- NEVER use the pipe character.
- NEVER create columns.
- NEVER use ASCII tables.
- NEVER use table separator lines.
- Do not place multiple unrelated ideas in one paragraph.

Return only the answer text.
"""

        answer = ask_llm(
            general_system_prompt,
            request.message
        )

        answer=clean_llm_formatting(answer)

        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )

        return {
            "message": answer
        }
    

    # ========================================================
    # OUT OF SCOPE
    # ========================================================

    if intent == "OUT_OF_SCOPE":

        answer = (
            "I'm designed to help with workplace compliance "
            "and regulatory questions. I can help you explore "
            "regulations, Acts, compliance particulars, "
            "applicability, and related requirements across "
            "countries and industries."
        )

        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )

        return {
            "message": answer
        }
    
    # ========================================================
    # APPLICABILITY QUERY
    # ========================================================

    if intent == "APPLICABILITY_QUERY":

        country = (
            route.get("country")
            or state.get("country")
        )

        industry = (
            route.get("industry")
            or state.get("industry")
        )

        requested_act =(
            route.get("act")
            or state.get("current_act")
            or state.get("act")
        ) 


        # --------------------------------------------
        # VALIDATE CONTEXT
        # --------------------------------------------

        if not country:

            answer = (
                "Which country would you like me to check?"
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }


        if not industry:

            answer = (
                "Which industry would you like me to check?"
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }


        if not requested_act:

            answer = (
                "Which Act would you like me to check "
                "for applicability?"
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }


        # --------------------------------------------
        # GET ALL AVAILABLE ACTS
        # --------------------------------------------

        all_acts = get_all_acts(
            country,
            db
        )

        # --------------------------------------------
        # FALLBACK: DETECT ACT FROM USER MESSAGE
        # --------------------------------------------

        if not requested_act:

            user_message_lower = request.message.lower()

            for act in all_acts:

                if act.lower() in user_message_lower:

                    requested_act = act
                    break


        # --------------------------------------------
        # MATCH ACT CASE-INSENSITIVELY
        # --------------------------------------------

        matched_act = None

        for act in all_acts:

            if act.strip().lower() == requested_act.strip().lower():

                matched_act = act
                break


        # --------------------------------------------
        # ACT NOT FOUND
        # --------------------------------------------

        if not matched_act:

            answer = (
                f"I couldn't find **{requested_act}** "
                f"in the available compliance database for "
                f"{country}."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }


        # --------------------------------------------
        # CHECK APPROVED MAPPING
        # --------------------------------------------

        approved_acts = get_mapping(
            country,
            industry,
            db
        )


        if matched_act in approved_acts:

            answer = (
                f"Yes. **{matched_act}** is currently listed "
                f"as applicable to the **{industry}** industry "
                f"in **{country}**."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer,
                "applicable": True,
                "status": "approved"
            }


        # --------------------------------------------
        # VERIFY THE ACT
        # --------------------------------------------

        verification = verify_mapping(
            country,
            industry,
            matched_act,
            all_acts
        )


        # --------------------------------------------
        # NOT APPLICABLE
        # --------------------------------------------

        if not verification.get("applicable"):

            answer = (
                f"Based on the available compliance data, "
                f"**{matched_act}** does not currently appear "
                f"applicable to the **{industry}** industry "
                f"in **{country}**.\n\n"
                f"Reason: {verification.get('reason', 'No reason available.')}"
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer,
                "applicable": False,
                "reason": verification.get("reason")
            }


        # --------------------------------------------
        # POTENTIALLY APPLICABLE → PENDING REVIEW
        # --------------------------------------------

        suggestion = save_suggestion(
            country,
            industry,
            matched_act,
            verification,
            db
        )


        answer = (
            f"**{matched_act}** appears potentially applicable "
            f"to the **{industry}** industry in **{country}**.\n\n"
            f"However, it is not currently part of the approved "
            f"compliance mapping. I've submitted it for "
            f"**admin review**."
        )


        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )


        return {
            "message": answer,
            "applicable": True,
            "status": suggestion.status,
            "confidence": verification.get("confidence"),
            "reason": verification.get("reason")
        }

    # ========================================================
    # FOLLOW-UP
    # ========================================================

    if intent == "FOLLOW_UP":

        context = {
            "country": state.get("country"),
            "industry": state.get("industry"),

            "current_act": state.get(
                "current_act",
                state.get("act")
            ),

            "current_particular": state.get(
                "current_particular"
            ),

            "available_acts": state.get(
                "acts",
                []
            ),

            "available_particulars": state.get(
                "particulars",
                []
            )
        }


        compliance_context = {}


        current_act = context.get(
            "current_act"
        )

        current_particular = context.get(
            "current_particular"
        )


        # ====================================================
        # CASE 1:
        # USER IS ASKING ABOUT A PARTICULAR
        # ====================================================

        if current_act and current_particular:

            result = get_description(
                current_act,
                current_particular,
                db
            )

            if result:

                compliance_context = {

                    "type": "particular",

                    "act": current_act,

                    "particular": current_particular,

                    "description":
                        result["description"]
                }


        # ====================================================
        # CASE 2:
        # USER IS ASKING ABOUT THE ACT GENERALLY
        # ====================================================

        elif current_act:

            particulars = get_particulars(
                current_act,
                db
            )


            act_information = []


            for particular in particulars:

                result = get_description(
                    current_act,
                    particular,
                    db
                )


                if result:

                    act_information.append({

                        "particular":
                            result["particular"],

                        "description":
                            result["description"]

                    })


            compliance_context = {

                "type": "act",

                "act": current_act,

                "compliance_requirements":
                    act_information
            }


        # ====================================================
        # GENERATE NATURAL RESPONSE
        # ====================================================

        answer = answer_follow_up(

            request.message,

            history,

            context,

            compliance_context

        )


        persist_exchange(

            session_id,

            request.message,

            answer,

            db

        )


        return {

            "message": answer

        }
        
    # ========================================================
    # CHANGE COUNTRY
    # ========================================================

    if intent == "CHANGE_COUNTRY":

        new_country = route.get(
            "country"
        )

        if not new_country:

            return {
                "message":
                    "Sure. Which country would you like to explore?"
            }

        industry = (
            route.get("industry")
            or state.get("industry")
        )

        if not industry:

            return {
                "message": (
                    f"Sure. Which industry would you like "
                    f"to explore in {new_country}?"
                )
            }

        # ----------------------------------------------------
        # Check cached mapping
        # ----------------------------------------------------

        cached_acts = get_mapping(
            new_country,
            industry,
            db
        )

        if cached_acts:

            applicable_acts = cached_acts

            print("\nUsing Cached Mapping")

        else:

            print("\nNo Mapping Found")

            all_acts = get_all_acts(
                new_country,
                db
            )

            applicable_acts = find_applicable_acts(
                new_country,
                industry,
                all_acts
            )

            if not applicable_acts:

                answer = (
                    f"I couldn't find applicable Acts in the "
                    f"available database for {industry} in "
                    f"{new_country}."
                )

                persist_exchange(
                    session_id,
                    request.message,
                    answer,
                    db
                )

                return {
                    "message": answer
                }

            save_mapping(
                new_country,
                industry,
                applicable_acts,
                db
            )

        # ----------------------------------------------------
        # Update state
        # ----------------------------------------------------

        update_state(
            session_id,
            {
                "step": "awaiting_act",
                "country": new_country,
                "industry": industry,
                "acts": applicable_acts,
                "current_act": None,
                "current_particular": None,
                "particulars": []
            }
        )

        assistant_message = (
            f"Sure. Let's look at {industry} compliance "
            f"in {new_country}. "
            f"I found the following potentially applicable Acts:"
        )

        persist_exchange(
            session_id,
            request.message,
            assistant_message,
            db,
            {
                "country": new_country,
                "industry": industry,
                "applicable_acts": applicable_acts,
                "next_step": "act_selection"
            }
        )

        return {
            "message": assistant_message,
            "country": new_country,
            "industry": industry,
            "applicable_acts": applicable_acts,
            "next_step": "act_selection"
        }

    # ========================================================
    # CHANGE INDUSTRY
    # ========================================================

    if intent == "CHANGE_INDUSTRY":

        new_industry = route.get(
            "industry"
        )

        if not new_industry:

            return {
                "message":
                    "Sure. Which industry would you like to explore?"
            }

        country = (
            route.get("country")
            or state.get("country")
        )

        if not country:

            return {
                "message": (
                    f"Sure. Which country should I use "
                    f"for {new_industry}?"
                )
            }

        # ----------------------------------------------------
        # Cached mapping
        # ----------------------------------------------------

        cached_acts = get_mapping(
            country,
            new_industry,
            db
        )

        if cached_acts:

            applicable_acts = cached_acts

            print("\nUsing Cached Mapping")

        else:

            print("\nNo Mapping Found")

            all_acts = get_all_acts(
                country,
                db
            )

            applicable_acts = find_applicable_acts(
                country,
                new_industry,
                all_acts
            )

            if not applicable_acts:

                answer = (
                    f"I couldn't find applicable Acts in the "
                    f"available database for {new_industry} "
                    f"in {country}."
                )

                persist_exchange(
                    session_id,
                    request.message,
                    answer,
                    db
                )

                return {
                    "message": answer
                }

            save_mapping(
                country,
                new_industry,
                applicable_acts,
                db
            )

        # ----------------------------------------------------
        # Update state
        # ----------------------------------------------------

        update_state(
            session_id,
            {
                "step": "awaiting_act",
                "country": country,
                "industry": new_industry,
                "acts": applicable_acts,
                "current_act": None,
                "current_particular": None,
                "particulars": []
            }
        )

        assistant_message = (
            f"Sure. Let's look at compliance requirements "
            f"for {new_industry} in {country}. "
            f"I found the following potentially applicable Acts:"
        )

        persist_exchange(
            session_id,
            request.message,
            assistant_message,
            db,
            {
                "country": country,
                "industry": new_industry,
                "applicable_acts": applicable_acts,
                "next_step": "act_selection"
            }
        )

        return {
            "message": assistant_message,
            "country": country,
            "industry": new_industry,
            "applicable_acts": applicable_acts,
            "next_step": "act_selection"
        }

    # ========================================================
    # SUGGESTION
    # ========================================================

    if intent == "SUGGESTION":

        # ----------------------------------------------------
        # GET CURRENT COUNTRY AND INDUSTRY CONTEXT
        # ----------------------------------------------------

        country = (
            route.get("country")
            or state.get("country")
        )

        industry = (
            route.get("industry")
            or state.get("industry")
        )

        # ----------------------------------------------------
        # VALIDATE CONTEXT
        # ----------------------------------------------------

        if not country or not industry:

            answer = (
                "Please first select a country and industry "
                "before suggesting an Act."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        # ----------------------------------------------------
        # DETECT SUGGESTED ACT
        # ----------------------------------------------------

        suggested_act = (
            route.get("act")
            or detect_suggestion(request.message)
        )

        if not suggested_act:

            answer = (
                "Which Act or regulation would you like to suggest?"
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        # ----------------------------------------------------
        # GET AVAILABLE ACTS
        # ----------------------------------------------------

        available_acts = get_all_acts(
            country,
            db
        )

        # ----------------------------------------------------
        # MATCH ACT CASE-INSENSITIVELY
        # ----------------------------------------------------

        matched_act = None

        for act in available_acts:

            if (
                act.strip().lower()
                ==
                suggested_act.strip().lower()
            ):

                matched_act = act
                break

        # ----------------------------------------------------
        # ACT NOT FOUND
        # ----------------------------------------------------

        if not matched_act:

            answer = (
                f"I couldn't find **{suggested_act}** "
                f"in the available compliance database for "
                f"{country}. Please suggest an Act that exists "
                f"in the available database."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        # ----------------------------------------------------
        # CHECK IF ALREADY APPROVED
        # ----------------------------------------------------

        approved_acts = get_mapping(
            country,
            industry,
            db
        )

        if matched_act in approved_acts:

            answer = (
                f"**{matched_act}** is already listed as applicable "
                f"to the **{industry}** industry in **{country}**."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer,
                "status": "ALREADY_APPROVED"
            }

        # ----------------------------------------------------
        # VERIFY SUGGESTION USING AI
        # ----------------------------------------------------

        verification = verify_mapping(
            country,
            industry,
            matched_act,
            available_acts
        )

        # ----------------------------------------------------
        # NOT APPLICABLE
        # ----------------------------------------------------

        if not verification.get("applicable"):

            answer = (
                f"Based on the verification, **{matched_act}** "
                f"does not appear applicable to the "
                f"**{industry}** industry in **{country}**.\n\n"
                f"Reason: "
                f"{verification.get('reason', 'No reason available.')}"
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer,
                "applicable": False,
                "reason": verification.get("reason")
            }

        # ----------------------------------------------------
        # SAVE AS PENDING ADMIN SUGGESTION
        # ----------------------------------------------------

        suggestion = save_suggestion(
            country,
            industry,
            matched_act,
            verification,
            db
        )

        answer = (
            f"Thank you! **{matched_act}** appears potentially "
            f"applicable to the **{industry}** industry in "
            f"**{country}**.\n\n"
            f"The suggestion has been submitted for "
            f"**admin review**."
        )

        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )

        return {
            "message": answer,
            "applicable": True,
            "confidence": verification.get("confidence"),
            "reason": verification.get("reason"),
            "status": suggestion.status
        }
    # ========================================================
    # INDUSTRY SELECTION
    # ========================================================

    if (
        state.get("step") == "awaiting_industry"
        and intent == "INDUSTRY_SELECTION"
    ):

        # Get industry from router, otherwise use clicked button text
        selected_industry = (
            route.get("industry")
            or request.message.strip()
        )

        available_industries = state.get(
            "available_industries",
            []
        )

        # ----------------------------------------------------
        # MATCH INDUSTRY CASE-INSENSITIVELY
        # ----------------------------------------------------

        matched_industry = None

        for industry in available_industries:

            if (
                industry.strip().lower()
                ==
                selected_industry.strip().lower()
            ):

                matched_industry = industry
                break

        # ----------------------------------------------------
        # INVALID INDUSTRY
        # ----------------------------------------------------

        if not matched_industry:

            return {
                "message":
                    "Please select one of the available industries.",
                "industries":
                    available_industries,
                "next_step":
                    "industry_selection"
            }

        selected_industry = matched_industry

        country = state.get("country")

        # ----------------------------------------------------
        # GET APPLICABLE ACTS
        # ----------------------------------------------------

        cached_acts = get_mapping(
            country,
            selected_industry,
            db
        )

        if cached_acts:

            print("\nUsing Cached Mapping")

            applicable_acts = cached_acts

        else:

            print("\nNo Mapping Found")

            all_acts = get_all_acts(
                country,
                db
            )

            print("\nAll Available Acts:")
            print(all_acts)

            applicable_acts = find_applicable_acts(
                country,
                selected_industry,
                all_acts
            )

            if not applicable_acts:

                answer = (
                    f"I couldn't find applicable Acts in the "
                    f"available database for the "
                    f"{selected_industry} industry in {country}."
                )

                persist_exchange(
                    session_id,
                    request.message,
                    answer,
                    db
                )

                return {
                    "message": answer
                }

            save_mapping(
                country,
                selected_industry,
                applicable_acts,
                db
            )

        # ----------------------------------------------------
        # UPDATE STATE
        # ----------------------------------------------------

        update_state(
            session_id,
            {
                "step": "awaiting_act",
                "country": country,
                "industry": selected_industry,
                "available_industries": available_industries,
                "acts": applicable_acts,
                "current_act": None,
                "current_particular": None,
                "particulars": []
            }
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        assistant_message = (
            f"Sure! Let's explore compliance requirements for "
            f"the {selected_industry} industry in {country}. "
            f"I found the following potentially applicable Acts:"
        )

        persist_exchange(
            session_id,
            request.message,
            assistant_message,
            db
        )

        return {
            "message": assistant_message,
            "country": country,
            "industry": selected_industry,
            "applicable_acts": applicable_acts,
            "next_step": "act_selection"
        }
        
    

    # ========================================================
    # ACT SELECTION
    # ========================================================

    if (
        state.get("step") == "awaiting_act"
        and intent == "ACT_SELECTION"
    ):

        selected_act = route.get(
            "act"
        )

        if not selected_act:

            selected_act = (
                request.message.strip()
            )

        available_acts = state.get(
            "acts",
            []
        )

        matched_act = None

        for act in available_acts:

            if act.lower() == selected_act.lower():

                matched_act = act
                break

        if not matched_act:

            return {
                "message":
                    "Please select one of the applicable Acts.",
                "applicable_acts":
                    available_acts
            }

        selected_act = matched_act

        particulars = sorted(
            set(
                p
                for p in get_particulars(
                    selected_act,
                    db
                )
                if p and p.strip()
            )
        )

        if not particulars:

            answer = (
                f"I couldn't find any compliance particulars "
                f"for the {selected_act} in the available database."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        country = state.get(
            "country"
        )

        industry = state.get(
            "industry"
        )

        update_state(
            session_id,
            {
                "step": "awaiting_particular",
                "country": country,
                "industry": industry,
                "act": selected_act,
                "current_act": selected_act,
                "current_particular": None,
                "particulars": particulars
            }
        )

        assistant_message = (
            f"Sure! Let's explore the **{selected_act}**.\n\n"
            f"I found the following compliance particulars "
            f"associated with this Act:\n\n"
            f"Please select a particular below to learn what "
            f"it means and why it is required."
        )

        persist_exchange(
            session_id,
            request.message,
            assistant_message,
            db
        )

        return {
            "message": assistant_message,
            "act": selected_act,
            "particulars": particulars,
            "next_step": "particular_selection"
        }

    # ========================================================
    # PARTICULAR SELECTION
    # ========================================================

    if (
        state.get("step")
        in [
            "awaiting_particular",
            "exploring_particular"
        ]
        and intent == "PARTICULAR_SELECTION"
    ):

        selected_particular = route.get(
            "particular"
        )

        if not selected_particular:

            selected_particular = (
                request.message.strip()
            )

        available_particulars = state.get(
            "particulars",
            []
        )

        matched_particular = None

        for particular in available_particulars:

            if (
                particular.strip().lower()
                ==
                selected_particular.strip().lower()
            ):

                matched_particular = particular
                break

        if not matched_particular:

            return {
                "message":
                    "Please select one of the available "
                    "compliance particulars.",
                "particulars":
                    available_particulars
            }

        current_act = state.get(
            "current_act",
            state.get("act")
        )

        result = get_description(
            current_act,
            matched_particular,
            db
        )

        if not result:

            answer = (
                f"No description found for "
                f"'{matched_particular}' under "
                f"'{current_act}'."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        assistant_message = (
            f"Sure! Here's what "
            f"{result['particular']} means under "
            f"the {current_act}:\n\n"
            f"{result['description']}\n\n"
            f"Would you like to explore another particular "
            f"under this Act? You can select one below, "
            f"or ask me a follow-up question."
        )

        update_state(
            session_id,
            {
                "step": "exploring_particular",
                "country": state.get("country"),
                "industry": state.get("industry"),
                "act": current_act,
                "current_act": current_act,
                "current_particular": result["particular"],
                "particulars": available_particulars
            }
        )

        persist_exchange(
            session_id,
            request.message,
            assistant_message,
            db
        )

        return {
            "message": assistant_message,
            "act": current_act,
            "particular": result["particular"],
            "description": result["description"],
            "particulars": available_particulars,
            "next_step": "particular_selection"
        }

    # ========================================================
    # CONTEXT RESOLUTION
    # ========================================================

    resolved_message = resolve_context(
        request.message,
        history
    )

    print("\nOriginal Message:")
    print(request.message)

    print("\nResolved Message:")
    print(resolved_message)

    # ========================================================
    # TOPIC VALIDATION
    # ========================================================

    
    # ========================================================
    # ENTITY EXTRACTION
    # ========================================================

    entities = {
        "country":
            resolved_message["country"],

        "industry":
            resolved_message["industry"]
    }

    # ========================================================
    # COUNTRY CHECK
    # ========================================================

    if not entities["country"]:

        answer = (
            "Sure. Which country would you like "
            "to explore?"
        )

        persist_exchange(
            session_id,
            request.message,
            answer,
            db
        )

        return {
            "message": answer
        }

    # ========================================================
    # INDUSTRY CHECK / INDUSTRY SELECTION
    # ========================================================

    if not entities["industry"]:

        country = entities["country"]

        available_industries = get_industries_by_country(
            country,
            db
        )

        if not available_industries:

            answer = (
                f"I couldn't find any industries in the available "
                f"database for {country}."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        # ----------------------------------------------------
        # UPDATE STATE
        # ----------------------------------------------------

        update_state(
            session_id,
            {
                "step": "awaiting_industry",
                "country": country,
                "industry": None,
                "available_industries": available_industries,
                "acts": [],
                "current_act": None,
                "current_particular": None,
                "particulars": []
            }
        )

        assistant_message = (
            f"Sure! Please select the industry you would like "
            f"to explore in {country}."
        )

        persist_exchange(
            session_id,
            request.message,
            assistant_message,
            db
        )

        return {
            "message": assistant_message,
            "country": country,
            "industries": available_industries,
            "next_step": "industry_selection"
        }

    # ========================================================
    # ACT RETRIEVAL
    # ========================================================

    country = entities["country"]
    industry = entities["industry"]

    print("\nFinal Country:", country)
    print("Final Industry:", industry)

    cached_acts = get_mapping(
        country,
        industry,
        db
    )

    if cached_acts:

        print("\nUsing Cached Mapping")

        applicable_acts = cached_acts

    else:

        print("\nNo Mapping Found")

        all_acts = get_all_acts(
            country,
            db
        )

        print("\n========== ACT DEBUG ==========")
        print("Country:", country)
        print("Industry:", industry)
        print("All Acts Found:", all_acts)

        applicable_acts = find_applicable_acts(
            country,
            industry,
            all_acts
        )

        print("Applicable Acts:", applicable_acts)
        print("================================")

        if not applicable_acts:

            answer = (
                f"No applicable Acts were found in the "
                f"database for the {industry} industry "
                f"in {country}."
            )

            persist_exchange(
                session_id,
                request.message,
                answer,
                db
            )

            return {
                "message": answer
            }

        save_mapping(
            country,
            industry,
            applicable_acts,
            db
        )

    # ========================================================
    # UPDATE STATE
    # ========================================================

    update_state(
        session_id,
        {
            "step": "awaiting_act",
            "country": country,
            "industry": industry,
            "acts": applicable_acts,
            "current_act": None,
            "current_particular": None,
            "particulars": []
        }
    )

    # ========================================================
    # NATURAL INITIAL COMPLIANCE RESPONSE
    # ========================================================

    assistant_message = (
        f"Sure! I've researched the compliance information "
        f"available for the {industry} industry in {country}.\n\n"
        f"Based on the available data, I found the following "
        f"Acts that appear applicable.\n\n"
        f"Select an Act below if you'd like to explore its "
        f"compliance particulars."
    )

    persist_exchange(
        session_id,
        request.message,
        assistant_message,
        db,
        {
            "country": country,
            "industry": industry,
            "applicable_acts": applicable_acts,
            "next_step": "act_selection"
        }
    )
    
    return {
        "message": assistant_message,
        "country": country,
        "industry": industry,
        "applicable_acts": applicable_acts,
        "next_step": "act_selection"
    }
           