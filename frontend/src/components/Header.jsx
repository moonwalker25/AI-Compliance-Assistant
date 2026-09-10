function Header() {
    return (
        <header className="h-16 border-b border-slate-200 bg-white/80 backdrop-blur-md">
            
            <div className="h-full flex items-center justify-between px-6">

                {/* LEFT SIDE */}

                <div className="flex items-center gap-3">

                    {/* AI ICON */}

                    <div className="
                        w-9 h-9
                        rounded-xl
                        bg-slate-900
                        text-white
                        flex
                        items-center
                        justify-center
                        shadow-sm
                    ">
                        🛡️
                    </div>


                    {/* TITLE */}

                    <div>

                        <h1 className="text-sm font-semibold text-slate-900">
                            ComplianceAI
                        </h1>

                        <p className="text-xs text-slate-500">
                            Enterprise Compliance Assistant
                        </p>

                    </div>

                </div>


                {/* RIGHT SIDE */}

                <div className="
                    hidden
                    sm:flex
                    items-center
                    gap-2
                    text-xs
                    text-slate-500
                ">

                    <span className="
                        w-2
                        h-2
                        rounded-full
                        bg-green-500
                    "></span>

                    AI Assistant Online

                </div>

            </div>

        </header>
    );
}

export default Header;