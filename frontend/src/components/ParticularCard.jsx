function ParticularCard({ particular, onClick }) {

    return (

        <button

            onClick={() => onClick(particular)}

            className="
                rounded-full
                border
                border-pink-500
                px-5
                py-2
                text-sm
                font-medium
                hover:bg-pink-50
                hover:scale-105
                transition
            "

        >

            📋 {particular}

        </button>

    );

}

export default ParticularCard;