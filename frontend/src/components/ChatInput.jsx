import { useRef, useState } from "react";

function ChatInput({ onSend, loading }) {

    const [message, setMessage] = useState("");

    const textareaRef = useRef(null);


    // -----------------------------
    // AUTO RESIZE TEXTAREA
    // -----------------------------

    const handleChange = (e) => {

        setMessage(e.target.value);

        const textarea = e.target;

        textarea.style.height = "auto";

        textarea.style.height =
            `${Math.min(textarea.scrollHeight, 160)}px`;
    };


    // -----------------------------
    // SEND MESSAGE
    // -----------------------------

    const handleSend = () => {

        if (loading) return;

        const trimmedMessage = message.trim();

        if (!trimmedMessage) return;

        onSend(trimmedMessage);

        setMessage("");

        // Reset textarea height
        if (textareaRef.current) {

            textareaRef.current.style.height = "auto";

        }

    };


    // -----------------------------
    // KEYBOARD HANDLING
    // -----------------------------

    const handleKeyDown = (e) => {

        // ENTER → SEND
        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            handleSend();

        }

        // SHIFT + ENTER → NEW LINE
        // Default textarea behaviour handles this automatically
    };


    return (

        <div className="
            w-full
            bg-gradient-to-t
            from-[#f7f7f8]
            via-[#f7f7f8]
            to-transparent
            pt-6
            pb-5
            px-4
        ">

            <div className="
                max-w-4xl
                mx-auto
            ">

                {/* INPUT CONTAINER */}

                <div className="
                    flex
                    items-end
                    gap-3
                    bg-white
                    border
                    border-slate-200
                    rounded-2xl
                    px-4
                    py-3
                    shadow-sm
                    transition
                    focus-within:border-slate-400
                    focus-within:shadow-md
                ">

                    {/* TEXTAREA */}

                    <textarea
                        ref={textareaRef}

                        value={message}

                        onChange={handleChange}

                        onKeyDown={handleKeyDown}

                        placeholder="Ask about workplace compliance..."

                        rows={1}

                        className="
                            flex-1
                            resize-none
                            bg-transparent
                            outline-none
                            text-slate-800
                            placeholder:text-slate-400
                            leading-6
                            max-h-40
                            py-1
                        "
                    />


                    {/* SEND BUTTON */}

                    <button

                        onClick={handleSend}

                        disabled={!message.trim() || loading}

                        className={`
                            w-10
                            h-10
                            shrink-0
                            rounded-xl
                            flex
                            items-center
                            justify-center
                            transition
                            ${
                                message.trim()
                                    ? `
                                        bg-slate-900
                                        text-white
                                        hover:bg-slate-700
                                        shadow-sm
                                    `
                                    : `
                                        bg-slate-100
                                        text-slate-400
                                        cursor-not-allowed
                                    `
                            }
                        `}
                        title="Send message"
                    >
                        {loading ? "..." : "↑"}
                    </button>

                </div>


                {/* FOOTNOTE */}

                <p className="
                    text-center
                    text-xs
                    text-slate-400
                    mt-3
                ">
                    ComplianceAI can make mistakes. Verify important compliance information.
                </p>

            </div>

        </div>

    );
}

export default ChatInput;   