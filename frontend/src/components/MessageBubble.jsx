import ReactMarkdown from "react-markdown";

import ActCard from "./ActCard";
import ParticularCard from "./ParticularCard";
import IndustryCard from "./IndustryCard";


function MessageBubble({
    sender,
    message,
    messageData,
    onOptionClick
}) {

    const isUser = sender === "user";


    // ========================================================
    // SAFELY HANDLE MESSAGE DATA
    // ========================================================

    let parsedMessageData = {};

    if (messageData) {

        if (typeof messageData === "string") {

            try {
                parsedMessageData = JSON.parse(messageData);
            } catch (error) {

                console.error(
                    "Failed to parse message_data:",
                    error
                );

                parsedMessageData = {};
            }

        } else if (typeof messageData === "object") {

            parsedMessageData = messageData;

        }
    }


    // ========================================================
    // GET RESPONSE DATA
    // ========================================================

    const responseData =
        parsedMessageData ||
        (
            typeof message === "object"
                ? message
                : {}
        );


    // ========================================================
    // SAFELY EXTRACT MESSAGE TEXT
    // ========================================================

    const messageText =
        typeof message === "string"
            ? message
            : message?.message;


    return (

        <div
            className={`
                flex
                w-full
                mb-8
                ${
                    isUser
                        ? "justify-end"
                        : "justify-start"
                }
            `}
        >

            {/* ====================================================
                ASSISTANT MESSAGE
            ==================================================== */}

            {!isUser && (

                <div className="
                    flex
                    gap-4
                    max-w-4xl
                    w-full
                ">

                    {/* AI Avatar */}

                    <div
                        className="
                            shrink-0
                            w-9
                            h-9
                            rounded-xl
                            bg-slate-900
                            text-white
                            flex
                            items-center
                            justify-center
                            shadow-sm
                        "
                    >
                        🛡️
                    </div>


                    {/* AI Content */}

                    <div className="
                        flex-1
                        min-w-0
                        pt-1
                    ">

                        <p className="
                            text-sm
                            font-semibold
                            text-slate-700
                            mb-2
                        ">
                            ComplianceAI
                        </p>


                        {/* MESSAGE TEXT */}

                        {messageText && (

                            <div className="
                                prose
                                prose-slate
                                max-w-none
                                text-slate-700
                                leading-7

                                prose-headings:text-slate-900
                                prose-headings:font-semibold

                                prose-p:my-3

                                prose-ul:my-3
                                prose-ol:my-3

                                prose-li:my-1

                                prose-strong:text-slate-900
                            ">

                                <ReactMarkdown>
                                    {messageText}
                                </ReactMarkdown>

                            </div>

                        )}


                        {/* ====================================================
                            INDUSTRY SELECTION
                        ==================================================== */}

                        {responseData?.industries?.length > 0 && (

                            <div className="mt-5">

                                <h3 className="
                                    text-xl
                                    font-semibold
                                    mb-4
                                ">
                                    🏢 Select an Industry
                                </h3>


                                <div className="
                                    flex
                                    flex-wrap
                                    gap-3
                                ">

                                    {responseData.industries.map(
                                        (industry) => (

                                            <IndustryCard
                                                key={industry}
                                                industry={industry}
                                                onClick={onOptionClick}
                                            />

                                        )
                                    )}

                                </div>

                            </div>

                        )}


                        {/* ====================================================
                            APPLICABLE ACTS
                        ==================================================== */}

                        {responseData?.applicable_acts?.length > 0 && (

                            <div className="mt-6">

                                <div className="
                                    flex
                                    items-center
                                    gap-2
                                    mb-3
                                ">

                                    <span>📜</span>

                                    <h3 className="
                                        font-semibold
                                        text-slate-800
                                    ">
                                        Applicable Acts
                                    </h3>

                                </div>


                                <div className="
                                    grid
                                    grid-cols-1
                                    sm:grid-cols-2
                                    gap-3
                                ">

                                    {responseData.applicable_acts.map(
                                        (act) => (

                                            <ActCard
                                                key={act}
                                                act={act}
                                                onClick={onOptionClick}
                                            />

                                        )
                                    )}

                                </div>

                            </div>

                        )}


                        {/* ====================================================
                            COMPLIANCE PARTICULARS
                        ==================================================== */}

                        {responseData?.particulars?.length > 0 && (

                            <div className="mt-6">

                                <div className="
                                    flex
                                    items-center
                                    gap-2
                                    mb-3
                                ">

                                    <span>📋</span>

                                    <h3 className="
                                        font-semibold
                                        text-slate-800
                                    ">
                                        Compliance Particulars
                                    </h3>

                                </div>


                                <div className="
                                    grid
                                    grid-cols-1
                                    sm:grid-cols-2
                                    gap-3
                                ">

                                    {responseData.particulars.map(
                                        (particular) => (

                                            <ParticularCard
                                                key={particular}
                                                particular={particular}
                                                onClick={onOptionClick}
                                            />

                                        )
                                    )}

                                </div>

                            </div>

                        )}


                        {/* ====================================================
                            DESCRIPTION
                        ==================================================== */}

                        {responseData?.description && (

                            <div className="
                                mt-6
                                rounded-xl
                                border
                                border-slate-200
                                bg-slate-50
                                p-5
                            ">

                                <p className="
                                    font-semibold
                                    text-slate-800
                                    mb-3
                                ">

                                    📄 {responseData.particular}

                                </p>


                                <div className="
                                    prose
                                    prose-slate
                                    max-w-none
                                    text-slate-700
                                    leading-7

                                    prose-p:my-3
                                    prose-ul:my-3
                                    prose-ol:my-3
                                    prose-li:my-1
                                ">

                                    <ReactMarkdown>
                                        {responseData.description}
                                    </ReactMarkdown>

                                </div>

                            </div>

                        )}

                    </div>

                </div>

            )}


            {/* ====================================================
                USER MESSAGE
            ==================================================== */}

            {isUser && (

                <div className="
                    flex
                    items-end
                    gap-3
                    max-w-[70%]
                ">

                    <div className="
                        bg-slate-800
                        text-white
                        rounded-2xl
                        rounded-br-md
                        px-5
                        py-3
                        shadow-sm
                    ">

                        <p className="
                            leading-7
                            whitespace-pre-wrap
                        ">
                            {messageText}
                        </p>

                    </div>


                    {/* User Avatar */}

                    <div
                        className="
                            shrink-0
                            w-9
                            h-9
                            rounded-xl
                            bg-slate-200
                            text-slate-600
                            flex
                            items-center
                            justify-center
                        "
                    >
                        👤
                    </div>

                </div>

            )}

        </div>

    );

}


export default MessageBubble;