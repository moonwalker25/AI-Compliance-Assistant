function IndustryCard({
    industry,
    onClick
}) {

    return (

        <button
            onClick={() => onClick(industry)}
            className="
                px-5
                py-3
                rounded-xl
                border
                border-slate-200
                bg-white
                text-left
                shadow-sm
                hover:border-blue-500
                hover:shadow-md
                transition
            "
        >

            <div className="font-medium text-slate-800">

                🏢 {industry}

            </div>

        </button>

    );

}

export default IndustryCard;