import { SpinnerProps } from "@/interfaces";


const Spinner = ({style}: SpinnerProps) => {
    return (
        <div
            role="status"
            aria-hidden="true"
            style={style}
            className="w-8 h-8 animate-spin border-solid border-2 border-white
                border-t-gray-800 rounded-full"
        >
        </div>
    )
};
  
export default Spinner;