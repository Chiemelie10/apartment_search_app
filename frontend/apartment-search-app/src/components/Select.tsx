import { usePathname } from "next/navigation";
import { capitalize } from "@/utils";


const Select = (props: SelectProps) => {
    const {register, name, options, disabled, dataTestId, style, firstOptionLabel } = props;
    const pathname = usePathname();

    return (
        <select
            {...register(name)}
            disabled={disabled}
            data-testid={dataTestId}
            style={style}
            className={`
                ${pathname === "/" ?
                    `h-8 sm:h-10 w-full px-2 mt-2 rounded-md
                    border-[1px] border-gray-400 border-solid
                    text-base ${disabled ? "" : "hover:cursor-pointer"}`
                :   `h-8 sm:h-9 w-full px-2 rounded-md
                    text-base bg-gray-200 border-[1px] border-gray-400 border-solid
                    ${disabled ? "" : "hover:cursor-pointer"}`
            }`}
        >
            <option value="">
                {
                    `${
                        pathname === "/" ? "Any"
                            : firstOptionLabel ? firstOptionLabel
                            : name === "min_price" ? "Price from"
                            : name === "max_price" ? "Price to"
                            : name === "available_for" ? "Search options"
                            : name === "listing_type" ? "Listing type"
                            : name === "min_room" ? "Rooms from"
                            : name === "max_room" ? "Rooms to"
                            : name === "min_floor_num" ? "Floor from"
                            : name === "max_floor_num" ? "Floor to"
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
                                    className="text-base w-full"
                                >
                                    {value === "sale" ? "Buy"
                                        : value === "short_let" ? "Short let"
                                        : capitalize(value)}
                                </option>
                    } else if (name === "sort_type" && typeof(value) === "string") {
                        return <option 
                                    key={index}
                                    value={value}
                                    className="text-base w-full"
                                >
                                    {value === "price" ? "Lowest price"
                                        : value === "-price" ? "Highest price"
                                        : value === "created_at" ? "Least recent"
                                        : value === "-created_at" ? "Most recent"
                                        : value === "bedroom" ? "Least number of bedrooms"
                                        : value === "-bedroom" ? "Most number of bedrooms"
                                        : capitalize(value)}
                                </option>
                    } else if (typeof(value) === "string") {
                        return <option 
                                    key={index}
                                    value={value}
                                    className="text-base w-full"
                                >
                                    {capitalize(value)}
                                </option>
                    } else if (typeof(value) === "number") {
                        return <option 
                                    key={index}
                                    value={value}
                                    className="text-base w-full"
                                >
                                    {value}
                                </option>
                    } else if (typeof(value) === "object") {
                        return <option
                                    key={value.id}
                                    value={value.id}
                                    className="text-base w-full"
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
