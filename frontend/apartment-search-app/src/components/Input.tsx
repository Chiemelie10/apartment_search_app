import { Path, UseFormRegister } from "react-hook-form";
import { SearchFormData } from "@/interfaces";

interface InputProps {
    type: string,
    name: Path<SearchFormData>,
    register: UseFormRegister<SearchFormData>,
    id: string,
}

const Input = (props: InputProps) => {
    const {type, name, register, id} = props;

    // const { ref, onChange, ...rest } = register(name);

    return (
        <>
            <input
                id={id}
                type={type}
                {...register(name)}
            />
        </>
    )
}

export default Input;