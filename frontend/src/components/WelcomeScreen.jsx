function WelcomeScreen({ onPromptClick }) {

    const examplePrompts = [
        {
            icon: "🏥",
            title: "Healthcare Compliance",
            prompt:
                "What healthcare compliances apply in India?"
        },
        {
            icon: "🏭",
            title: "Manufacturing Regulations",
            prompt:
                "What workplace compliances apply to the manufacturing industry in India?"
        },
        {
            icon: "🌍",
            title: "Explore Another Country",
            prompt:
                "What workplace compliance requirements apply in France?"
        },
        {
            icon: "📋",
            title: "Understand an Act",
            prompt:
                "Tell me about the ESI Act and its compliance requirements."
        }
    ];


    return (

        <div className="
            flex-1
            flex
            flex-col
            items-center
            justify-center
            px-6
            py-10
        ">

            {/* Hero */}

            <div className="
                text-center
                max-w-2xl
                mb-10
            ">

                <div className="
                    w-16
                    h-16
                    mx-auto
                    mb-5
                    rounded-2xl
                    bg-slate-900
                    text-white
                    flex
                    items-center
                    justify-center
                    text-2xl
                    shadow-lg
                ">
                    🛡️
                </div>


                <h1 className="
                    text-3xl
                    md:text-4xl
                    font-bold
                    text-slate-900
                ">
                    How can I help with compliance today?
                </h1>


                <p className="
                    mt-4
                    text-slate-500
                    leading-7
                ">

                    ComplianceAI helps you explore workplace
                    compliance requirements across countries and
                    industries through context-aware conversations.

                </p>

            </div>


            {/* Example Prompts */}

            <div className="
                w-full
                max-w-3xl
            ">

                <p className="
                    text-xs
                    font-semibold
                    uppercase
                    tracking-wider
                    text-slate-400
                    mb-4
                ">
                    Try asking
                </p>


                <div className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    gap-4
                ">

                    {examplePrompts.map(
                        (item, index) => (

                            <button
                                key={index}

                                onClick={() =>
                                    onPromptClick(
                                        item.prompt
                                    )
                                }

                                className="
                                    text-left
                                    bg-white
                                    border
                                    border-slate-200
                                    rounded-2xl
                                    p-5
                                    hover:border-slate-400
                                    hover:shadow-md
                                    transition
                                    group
                                "
                            >

                                <div className="
                                    flex
                                    items-start
                                    gap-4
                                ">

                                    <div className="
                                        text-2xl
                                    ">
                                        {item.icon}
                                    </div>


                                    <div>

                                        <h3 className="
                                            font-semibold
                                            text-slate-800
                                            group-hover:text-slate-950
                                        ">
                                            {item.title}
                                        </h3>


                                        <p className="
                                            text-sm
                                            text-slate-500
                                            mt-1
                                            leading-6
                                        ">
                                            {item.prompt}
                                        </p>

                                    </div>

                                </div>

                            </button>

                        )
                    )}

                </div>

            </div>


            {/* Footer note */}

            <p className="
                mt-8
                text-xs
                text-slate-400
                text-center
            ">
                ComplianceAI provides compliance information and
                should not be considered professional legal advice.
            </p>

        </div>

    );
}


export default WelcomeScreen;