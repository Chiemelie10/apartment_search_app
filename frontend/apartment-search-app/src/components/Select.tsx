import { Path, UseFormRegister } from "react-hook-form";
import { SearchFormData } from "@/interfaces";
import { usePathname } from "next/navigation";
import { capitalize } from "@/utils";


interface SelectProps {
    name: Path<SearchFormData>;
    register: UseFormRegister<SearchFormData>;
    id: string;
    options: { name: string, id: string }[] | number[] | string[] | undefined;
    disabled?: boolean;
    handleChange?: () => void;
}

const Select = (props: SelectProps) => {
    const {register, name, options, disabled } = props;
    const pathname = usePathname();
    // const { onChange, ...rest } = register(name)
    // if (name === "city") console.log(options)

    return (
        <select
            {...register(name)}
            disabled={disabled}
            // onChange={(e) => {
            //     onChange(e);
            //     if (handleChange) {
            //         handleChange();
            //     }
            // }}
            className={`
                ${pathname === "/" ?
                    `h-8 sm:h-10 w-full px-2 py-0 sm:py-2 mt-2 rounded-sm
                    text-base font-serif
                    ${disabled ? "" : "hover:cursor-pointer"}`
                :   `h-8 sm:h-9 w-full px-2 py-0 sm:py-2 rounded-sm
                    text-base font-serif bg-gray-200
                    ${disabled ? "" : "hover:cursor-pointer"}`
            }`}
        >
            <option value="">
                {
                    `${
                        pathname === "/" ? "Any"
                            : name === "min_price" ? "Price from"
                            : name === "max_price" ? "Price to"
                            : name === "available_for" ? "Search option"
                            : name === "sort_type" ? "Select..."
                            : capitalize(name)
                    }`
                }
            </option>
            {
                options?.map((value, index) => {
                    if (name === "available_for" && typeof(value) === "string") {
                        return <option 
                                    key={index}
                                    value={value}
                                    className="text-base font-serif w-full"
                                >
                                    {value === "sale" ? "Buy"
                                        : value === "short_let" ? "Short let"
                                        : capitalize(value)}
                                </option>
                    } else if (typeof(value) === "string") {
                        return <option 
                                    key={index}
                                    value={value}
                                    className="text-base font-serif w-full"
                                >
                                    {capitalize(value)}
                                </option>
                    } else if (typeof(value) === "number") {
                        return <option 
                                    key={index}
                                    value={value}
                                    className="text-base font-serif w-full"
                                >
                                    {value}
                                </option>
                    } else if (typeof(value) === "object") {
                        return <option
                                    key={value.id}
                                    value={value.id}
                                    className="text-base font-serif w-full"
                                >
                                    {capitalize(value.name)}
                                </option>
                    }
                })
            }
      </select>
    )
}

export default Select;
