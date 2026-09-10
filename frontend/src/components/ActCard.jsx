function ActCard({ act, onClick }) {

    return (

        <button

            onClick={() => onClick(act)}

            className="
            bg-white
            border
            border-slate-200
            rounded-xl
            px-5
            py-4
            shadow-sm
            hover:shadow-lg
            hover:border-blue-500
            hover:-translate-y-1
            transition
            duration-200
            flex
            items-center
            gap-3
            "

        >

            <span className="text-xl">

                📜

            </span>

            <span className="font-medium">

                {act}

            </span>

        </button>

    );

}

export default ActCard;