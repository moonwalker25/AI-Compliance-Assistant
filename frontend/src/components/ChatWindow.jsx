import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";


function ChatWindow({
    messages,
    onOptionClick
}) {

    const bottomRef = useRef(null);


    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages]);


    return (

        <div className="
            flex-1
            overflow-y-auto
            scroll-smooth
        ">

            <div className="
                max-w-4xl
                mx-auto
                px-6
                py-8
            ">

                {messages.map(
                    (msg, index) => (

                        <MessageBubble
                            key={index}
                            sender={msg.sender}
                            message={msg.message}
                            messageData={msg.message_data}
                            onOptionClick={
                                onOptionClick
                            }
                        />

                    )
                )}


                <div ref={bottomRef} />

            </div>

        </div>

    );

}


export default ChatWindow;