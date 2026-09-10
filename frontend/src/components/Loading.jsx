function Loading() {

    return (

        <div className="w-full bg-slate-50">

            <div className="max-w-4xl mx-auto px-6 py-6">

                <div className="flex gap-4">

                    <div className="
                        w-9
                        h-9
                        rounded-lg
                        bg-blue-600
                        text-white
                        flex
                        items-center
                        justify-center
                        font-semibold
                    ">
                        AI
                    </div>


                    <div className="
                        flex
                        items-center
                        gap-1
                        bg-white
                        border
                        border-slate-200
                        rounded-xl
                        px-4
                        py-3
                    ">

                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>

                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></span>

                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></span>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Loading;