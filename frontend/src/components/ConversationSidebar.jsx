import { useEffect, useState, useRef } from "react";

import {
    getConversations,
    deleteConversation,
} from "../services/api";


function ConversationSidebar({
    currentSessionId,
    onSelectConversation,
    onNewChat,
    refreshKey,

    isOpen,
    onClose,
}) {

    // ========================================================
    // CONVERSATIONS
    // ========================================================

    const [conversations, setConversations] =
        useState([]);

    const [loading, setLoading] =
        useState(true);


    // ========================================================
    // SIDEBAR WIDTH
    // ========================================================

    const [sidebarWidth, setSidebarWidth] =
        useState(() => {

            const savedWidth =
                localStorage.getItem("sidebar_width");

            if (savedWidth) {

                const width =
                    Number(savedWidth);

                // Make sure saved width is valid
                if (width >= 220 && width <= 500) {
                    return width;
                }

            }

            return 288;

        });


    // ========================================================
    // RESIZING STATE
    // ========================================================

    const [isResizing, setIsResizing] =
        useState(false);

    const sidebarRef =
        useRef(null);


    // ========================================================
    // WIDTH LIMITS
    // ========================================================

    const MIN_WIDTH = 220;
    const MAX_WIDTH = 500;


    // ========================================================
    // LOAD CONVERSATIONS
    // ========================================================

    const loadConversations = async () => {

        try {

            const data =
                await getConversations();

            setConversations(data || []);

        } catch (error) {

            console.error(
                "Failed to load conversations:",
                error
            );

        } finally {

            setLoading(false);

        }

    };


    useEffect(() => {

        loadConversations();

    }, [refreshKey]);


    // ========================================================
    // SAVE SIDEBAR WIDTH
    // ========================================================

    useEffect(() => {

        localStorage.setItem(
            "sidebar_width",
            sidebarWidth.toString()
        );

    }, [sidebarWidth]);


    // ========================================================
    // START RESIZING
    // ========================================================

    const startResizing = (event) => {

        // Only allow mouse resizing on desktop/tablet
        if (window.innerWidth < 768) {
            return;
        }

        event.preventDefault();

        setIsResizing(true);

    };


    // ========================================================
    // HANDLE RESIZING
    // ========================================================

    useEffect(() => {

        const handleMouseMove = (event) => {

            if (!isResizing) return;

            let newWidth =
                event.clientX;


            // Minimum width
            if (newWidth < MIN_WIDTH) {

                newWidth = MIN_WIDTH;

            }


            // Maximum width
            if (newWidth > MAX_WIDTH) {

                newWidth = MAX_WIDTH;

            }


            setSidebarWidth(
                newWidth
            );

        };


        const stopResizing = () => {

            setIsResizing(false);

        };


        if (isResizing) {

            document.body.style.cursor =
                "col-resize";

            document.body.style.userSelect =
                "none";

        }


        window.addEventListener(
            "mousemove",
            handleMouseMove
        );


        window.addEventListener(
            "mouseup",
            stopResizing
        );


        return () => {

            window.removeEventListener(
                "mousemove",
                handleMouseMove
            );


            window.removeEventListener(
                "mouseup",
                stopResizing
            );


            document.body.style.cursor =
                "";

            document.body.style.userSelect =
                "";

        };

    }, [isResizing]);


    // ========================================================
    // DELETE CONVERSATION
    // ========================================================

    const handleDelete = async (
        e,
        sessionId
    ) => {

        e.stopPropagation();

        try {

            await deleteConversation(
                sessionId
            );

            setConversations((prev) =>
                prev.filter(
                    (conversation) =>
                        conversation.id !== sessionId
                )
            );

        } catch (error) {

            console.error(
                "Failed to delete conversation:",
                error
            );

        }

    };


    // ========================================================
    // SELECT CONVERSATION
    // ========================================================

    const handleSelect = (
        conversationId
    ) => {

        onSelectConversation(
            conversationId
        );


        // Close sidebar on mobile
        if (window.innerWidth < 768) {

            onClose?.();

        }

    };


    // ========================================================
    // NEW CHAT
    // ========================================================

    const handleNewConversation = () => {

        onNewChat();


        // Close sidebar on mobile
        if (window.innerWidth < 768) {

            onClose?.();

        }

    };


    return (

        <>

            {/* ====================================================
                MOBILE BACKDROP
            ==================================================== */}

            {isOpen && (

                <div
                    onClick={onClose}
                    className="
                        fixed
                        inset-0
                        bg-black/50
                        z-40
                        md:hidden
                    "
                />

            )}


            {/* ====================================================
                SIDEBAR
            ==================================================== */}

            <aside

                ref={sidebarRef}

                style={{
                    width: `${sidebarWidth}px`
                }}

                className={`
                    fixed
                    md:relative

                    inset-y-0
                    left-0

                    z-50

                    h-screen

                    bg-slate-950
                    text-white

                    flex
                    flex-col

                    border-r
                    border-slate-800

                    transition-transform
                    duration-300
                    ease-in-out

                    shrink-0

                    ${
                        isOpen
                            ? "translate-x-0"
                            : "-translate-x-full md:translate-x-0"
                    }
                `}
            >


                {/* ====================================================
                    MOBILE CLOSE BUTTON
                ==================================================== */}

                <button

                    onClick={onClose}

                    className="
                        md:hidden

                        absolute
                        top-4
                        right-4

                        w-8
                        h-8

                        rounded-lg

                        bg-slate-800

                        flex
                        items-center
                        justify-center

                        text-slate-300

                        hover:bg-slate-700

                        transition
                    "

                    aria-label="Close sidebar"
                >
                    ✕
                </button>


                {/* ====================================================
                    BRAND
                ==================================================== */}

                <div className="
                    px-5
                    py-5
                    border-b
                    border-slate-800
                ">

                    <div className="
                        flex
                        items-center
                        gap-3
                    ">

                        <div className="
                            w-9
                            h-9

                            rounded-xl

                            bg-white
                            text-slate-950

                            flex
                            items-center
                            justify-center

                            font-bold
                        ">
                            AI
                        </div>


                        <div>

                            <h1 className="
                                font-semibold
                                text-sm
                            ">
                                ComplianceAI
                            </h1>


                            <p className="
                                text-xs
                                text-slate-400
                            ">
                                Enterprise AI
                            </p>

                        </div>

                    </div>

                </div>


                {/* ====================================================
                    NEW CHAT
                ==================================================== */}

                <div className="p-4">

                    <button

                        onClick={
                            handleNewConversation
                        }

                        className="
                            w-full

                            flex
                            items-center
                            justify-center
                            gap-2

                            px-4
                            py-3

                            rounded-xl

                            bg-white
                            text-slate-900

                            font-medium
                            text-sm

                            hover:bg-slate-200

                            transition
                        "
                    >

                        <span className="text-lg">
                            +
                        </span>

                        New Chat

                    </button>

                </div>


                {/* ====================================================
                    ABOUT
                ==================================================== */}

                <div className="
                    px-4
                    pb-5
                ">

                    <div className="
                        rounded-xl

                        bg-slate-900

                        border
                        border-slate-800

                        p-4
                    ">

                        <p className="
                            text-xs
                            font-semibold

                            text-slate-400

                            uppercase

                            tracking-wider

                            mb-3
                        ">
                            About ComplianceAI
                        </p>


                        <p className="
                            text-sm
                            text-slate-300
                            leading-6
                        ">
                            Your AI-powered assistant for exploring
                            workplace compliance requirements across
                            different countries and industries.
                        </p>


                        <div className="
                            mt-4
                            space-y-2
                        ">

                            <div className="
                                flex
                                gap-2
                                text-xs
                                text-slate-400
                            ">
                                <span>✦</span>

                                <span>
                                    Understands conversation context
                                </span>
                            </div>


                            <div className="
                                flex
                                gap-2
                                text-xs
                                text-slate-400
                            ">
                                <span>✦</span>

                                <span>
                                    Explore applicable Acts and
                                    requirements
                                </span>
                            </div>


                            <div className="
                                flex
                                gap-2
                                text-xs
                                text-slate-400
                            ">
                                <span>✦</span>

                                <span>
                                    Country and industry aware
                                </span>
                            </div>

                        </div>

                    </div>

                </div>


                {/* ====================================================
                    HOW TO USE
                ==================================================== */}

                <div className="
                    px-4
                    pb-5
                ">

                    <p className="
                        text-xs
                        font-medium

                        text-slate-500

                        uppercase

                        tracking-wider

                        mb-3
                    ">
                        How to use
                    </p>


                    <div className="
                        space-y-2
                        text-xs
                        text-slate-400
                    ">

                        <p>
                            <span className="
                                text-slate-200
                                font-medium
                            ">
                                1.
                            </span>

                            {" "}
                            Ask about workplace compliance
                        </p>


                        <p>
                            <span className="
                                text-slate-200
                                font-medium
                            ">
                                2.
                            </span>

                            {" "}
                            Explore relevant Acts
                        </p>


                        <p>
                            <span className="
                                text-slate-200
                                font-medium
                            ">
                                3.
                            </span>

                            {" "}
                            Select requirements for details
                        </p>

                    </div>

                </div>


                {/* ====================================================
                    RECENT CONVERSATIONS TITLE
                ==================================================== */}

                <div className="
                    px-4
                    pb-2
                ">

                    <p className="
                        text-xs
                        font-medium

                        text-slate-500

                        uppercase

                        tracking-wider
                    ">
                        Recent conversations
                    </p>

                </div>


                {/* ====================================================
                    CONVERSATIONS
                ==================================================== */}

                <div className="
                    flex-1
                    overflow-y-auto
                    px-3
                ">

                    {loading ? (

                        <div className="
                            px-3
                            py-4
                            text-sm
                            text-slate-500
                        ">
                            Loading conversations...
                        </div>

                    ) : conversations.length === 0 ? (

                        <div className="
                            px-3
                            py-4
                            text-sm
                            text-slate-500
                        ">
                            No conversations yet.
                        </div>

                    ) : (

                        <div className="space-y-1">

                            {conversations.map(
                                (conversation) => (

                                    <div

                                        key={
                                            conversation.id
                                        }

                                        onClick={() =>
                                            handleSelect(
                                                conversation.id
                                            )
                                        }

                                        className={`
                                            group

                                            flex
                                            items-center
                                            gap-2

                                            px-3
                                            py-3

                                            rounded-lg

                                            cursor-pointer

                                            transition

                                            ${
                                                currentSessionId ===
                                                conversation.id

                                                    ? "bg-slate-800"

                                                    : "hover:bg-slate-900"
                                            }
                                        `}
                                    >

                                        <div className="
                                            flex-1
                                            min-w-0
                                        ">

                                            <p className="
                                                text-sm
                                                truncate
                                                text-slate-200
                                            ">
                                                {
                                                    conversation.title ||
                                                    "New Conversation"
                                                }
                                            </p>

                                        </div>


                                        <button

                                            onClick={(e) =>
                                                handleDelete(
                                                    e,
                                                    conversation.id
                                                )
                                            }

                                            className="
                                                opacity-0

                                                group-hover:opacity-100

                                                text-slate-500

                                                hover:text-red-400

                                                transition

                                                px-1
                                            "

                                            title="Delete conversation"
                                        >
                                            ×
                                        </button>

                                    </div>

                                )
                            )}

                        </div>

                    )}

                </div>


                {/* ====================================================
                    FOOTER
                ==================================================== */}

                <div className="
                    p-4

                    border-t
                    border-slate-800
                ">

                    <div className="
                        text-xs
                        text-slate-500
                    ">
                        Enterprise AI Compliance Assistant
                    </div>

                </div>


                {/* ====================================================
                    RESIZE HANDLE
                ==================================================== */}

                <div

                    onMouseDown={
                        startResizing
                    }

                    className={`
                        hidden
                        md:block

                        absolute
                        top-0
                        right-0

                        w-1
                        h-full

                        cursor-col-resize

                        z-[60]

                        transition-colors

                        ${
                            isResizing
                                ? "bg-blue-500"
                                : "hover:bg-blue-500"
                        }
                    `}

                    title="Drag to resize sidebar"
                />

            </aside>

        </>

    );

}


export default ConversationSidebar;