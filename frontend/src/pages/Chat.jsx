import { useState } from "react";

import WelcomeScreen from "../components/WelcomeScreen";
import Layout from "../components/Layout";
import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import Loading from "../components/Loading";
import ConversationSidebar from "../components/ConversationSidebar";

import {
    sendMessage,
    getConversation
} from "../services/api";


function Chat() {

    // =========================================================
    // SESSION ID
    // =========================================================

    const [sessionId, setSessionId] = useState(() => {

        const existingId =
            localStorage.getItem("chat_session_id");

        if (existingId) {
            return existingId;
        }

        const newId = crypto.randomUUID();

        localStorage.setItem(
            "chat_session_id",
            newId
        );

        return newId;
    });


    // =========================================================
    // MESSAGES
    // =========================================================

    const [messages, setMessages] = useState([]);


    // =========================================================
    // LOADING
    // =========================================================

    const [loading, setLoading] =
        useState(false);

    const [conversationRefresh, setConversationRefresh] =
        useState(0);

    const [loadingConversation, setLoadingConversation] =
        useState(false);
    
    // --------------------------------
    // SIDEBAR CONTROLS
     // --------------------------------

    const [sidebarOpen, setSidebarOpen] =
        useState(false);

    const [sidebarWidth, setSidebarWidth] =
        useState(288);
    
    // =========================================================
    // SEND MESSAGE
    // =========================================================

    const handleSend = async (text) => {

        if (!text.trim() || loading) {
            return;
        }


        // -----------------------------------------------------
        // ADD USER MESSAGE IMMEDIATELY
        // -----------------------------------------------------

        setMessages((prev) => [
            ...prev,
            {
                sender: "user",
                message: text,
                message_data: null
            }
        ]);


        setLoading(true);


        try {

            const response =
                await sendMessage(
                    text,
                    sessionId
                );


            console.log(
                "Backend response:",
                response
            );


            // -------------------------------------------------
            // BUILD UI DATA
            // -------------------------------------------------

            const messageData = {

                country:
                    response.country ?? null,

                industry:
                    response.industry ?? null,

                industries:
                    response.industries ?? null,

                applicable_acts:
                    response.applicable_acts ?? null,

                particulars:
                    response.particulars ?? null,

                next_step:
                    response.next_step ?? null
            };


            // -------------------------------------------------
            // ADD ASSISTANT MESSAGE
            // -------------------------------------------------

            setMessages((prev) => [
                ...prev,
                {
                    sender: "assistant",
                    message: response.message,
                    message_data: messageData
                }
            ]);


            // Refresh sidebar
            setConversationRefresh(
                (prev) => prev + 1
            );


        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


            setMessages((prev) => [
                ...prev,
                {
                    sender: "assistant",
                    message:
                        "❌ Unable to contact the backend. Please try again.",
                    message_data: null
                }
            ]);


        } finally {

            setLoading(false);

        }
    };


    // =========================================================
    // LOAD EXISTING CONVERSATION
    // =========================================================

    const handleSelectConversation =
        async (selectedSessionId) => {

            try {

                setLoadingConversation(true);

                setLoading(false);


                const conversation =
                    await getConversation(
                        selectedSessionId
                    );


                console.log(
                    "Loaded conversation:",
                    conversation
                );


                // -------------------------------------------------
                // UPDATE SESSION
                // -------------------------------------------------

                setSessionId(
                    selectedSessionId
                );


                localStorage.setItem(
                    "chat_session_id",
                    selectedSessionId
                );


                // -------------------------------------------------
                // RESTORE MESSAGES
                // -------------------------------------------------

                const restoredMessages =
                    conversation.messages.map((message) => {

                        let parsedMessageData =
                            message.message_data;


                        // Handle old records stored as strings
                        if (
                            typeof parsedMessageData === "string"
                        ) {

                            try {

                                parsedMessageData =
                                    JSON.parse(
                                        parsedMessageData
                                    );

                            } catch (error) {

                                console.error(
                                    "Failed to parse message_data:",
                                    error
                                );

                                parsedMessageData = null;
                            }
                        }


                        return {

                            sender:
                                message.sender,

                            message:
                                message.message,

                            message_data:
                                parsedMessageData ?? null
                        };

                    });


                console.log(
                    "Restored messages:",
                    restoredMessages
                );


                setMessages(
                    restoredMessages
                );


            } catch (error) {

                console.error(
                    "Failed to load conversation:",
                    error
                );


                setMessages([
                    {
                        sender: "assistant",

                        message:
                            "❌ Unable to load this conversation.",

                        message_data: null
                    }
                ]);


            } finally {

                setLoadingConversation(false);

            }

        };


    // =========================================================
    // NEW CHAT
    // =========================================================

    const handleNewChat = () => {

        const newSessionId =
            crypto.randomUUID();


        setSessionId(
            newSessionId
        );


        localStorage.setItem(
            "chat_session_id",
            newSessionId
        );


        setMessages([]);

        setLoading(false);

        setLoadingConversation(false);

    };


    // =========================================================
    // UI
    // =========================================================

    return (

        <Layout>

            <div className="flex h-screen">


                {/* =================================================
                    SIDEBAR
                ================================================= */}

                <ConversationSidebar

                    currentSessionId={sessionId}

                    onSelectConversation={
                        handleSelectConversation
                    }

                    onNewChat={
                        handleNewChat
                    }

                    refreshKey={
                        conversationRefresh
                    }
                    isOpen={
                        sidebarOpen
                    }
                
                    onClose={() =>
                        setSidebarOpen(false)
                    }
                
                    sidebarWidth={
                        sidebarWidth
                    }

                />


                {/* =================================================
                    MAIN CHAT
                ================================================= */}

                <div className="flex flex-col flex-1">

                <div className="flex items-center">

                    <button
                        onClick={() =>
                            setSidebarOpen(true)
                        }

                        className="
                            md:hidden

                            ml-4

                            w-10
                            h-10

                            flex
                            items-center
                            justify-center

                            rounded-lg

                            hover:bg-slate-100

                            text-xl

                            transition
                        "

                        aria-label="Open sidebar"
                    >
                        ☰
                    </button>

                    <div className="flex-1">
                        <Header />
                    </div>

                </div>


                    <div
                        className="
                            flex-1
                            flex
                            flex-col
                            w-full
                            overflow-hidden
                        "
                    >


                        {/* LOADING OLD CONVERSATION */}

                        {loadingConversation && (

                            <div
                                className="
                                    flex
                                    items-center
                                    justify-center
                                    py-3
                                    text-sm
                                    text-gray-500
                                "
                            >
                                Loading conversation...
                            </div>

                        )}


                        {/* CHAT CONTENT */}

                        {!loadingConversation && (

                            messages.length === 0 ? (

                                <WelcomeScreen
                                    onPromptClick={
                                        handleSend
                                    }
                                />

                            ) : (

                                <ChatWindow

                                    messages={
                                        messages
                                    }

                                    onOptionClick={
                                        handleSend
                                    }

                                />

                            )

                        )}


                        {/* AI RESPONSE LOADING */}

                        {loading && (

                            <Loading />

                        )}


                        {/* CHAT INPUT */}

                        <ChatInput

                            onSend={
                                handleSend
                            }

                            loading={
                                loading
                            }

                        />

                    </div>

                </div>

            </div>

        </Layout>

    );

}


export default Chat;