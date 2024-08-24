"use client";

import Select from "./Select";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { Search } from "react-feather";
import { useEffect } from "react";


const SearchBar = (props: SearchBarProps ) => {
    // This component displays a searchbar on pages it is used in.

    const {
        searchedOption,
        setSearchedOption,
        setMoreFilters,
        handleSubmit,
        register,
        setValue,
        states,
        cities,
        selectedState,
        selectedModalState,
        selectedModalCity,
        selectedModalMaxPrice,
        selectedModalMinPrice,
        selectedModalSearchedOption,
        priceRange,
        id,
        onSubmit
    } = props;

    const pathname = usePathname();

    useEffect(() => {
        setValue("state", selectedModalState)
    }, [selectedModalState, setValue])

    useEffect(() => {
        setValue("city", selectedModalCity)
    }, [selectedModalCity, setValue])

    useEffect(() => {
        setValue("min_price", selectedModalMinPrice)
    }, [selectedModalMinPrice, setValue])

    useEffect(() => {
        setValue("max_price", selectedModalMaxPrice)
    }, [selectedModalMaxPrice, setValue])

    useEffect(() => {
        if (pathname === "/") {
            if (selectedModalSearchedOption === "rent" || selectedModalSearchedOption === "sale"
                || selectedModalSearchedOption === "share") {
                setSearchedOption(selectedModalSearchedOption);
            }
        } else {
            if (selectedModalSearchedOption === "rent" || selectedModalSearchedOption === "sale"
                || selectedModalSearchedOption === "share" || selectedModalSearchedOption === "lease"
                || selectedModalSearchedOption === "short_let" || selectedModalSearchedOption === "") {
                setValue("available_for", selectedModalSearchedOption);
            }
        }
    }, [selectedModalSearchedOption, setSearchedOption])

    const handleMoreFilterClick = () => {
        setMoreFilters(true);
        document.body.style.overflow = "hidden";
    }


    return (
        <div className="flex flex-col text-base relative">
            {
                pathname === "/" && (
                    <div className="self-center mb-14">
                        <h1
                            className="text-lg mini:text-2xl lg:text-4xl font-bold
                                text-white shadow-sm">
                                    Find your dream home
                        </h1>
                    </div>
                )
            }
            {/* Searchbar */}
            <div
                className={`
                    w-full flex flex-col justify-start items-center
                    ${pathname === "/" ? "lg:px-10" : "lg:px-0"}
                `}
            >
                {
                    // Search options design for only home page
                    pathname === "/" && (
                        <div className="md:self-start h-16 bg-blue-950 rounded-t-xl
                            border-b-[1px] border-solid border-b-gray-500"
                        >
                            <ul className="flex h-full text-white divide-x divide-solid
                                divide-gray-600"
                            >
                                <li
                                    className={`min-w-[78px] rounded-tl-xl hover:opacity-80
                                        ${searchedOption === "sale"
                                            ? "bg-cyan-300 text-black" : ""
                                        }
                                    `}
                                >
                                    <Link
                                        href=""
                                        data-testid="SearchBar-buy"
                                        onClick={() => setSearchedOption("sale")}
                                        className="w-full h-full flex justify-center items-center"
                                        >
                                            Buy
                                    </Link>
                                </li>
                                <li
                                    className={`min-w-[78px] hover:opacity-80
                                        ${searchedOption === "rent"
                                            ? "bg-cyan-300 text-black" : ""
                                        }
                                    `}
                                >
                                    <Link
                                        href=""
                                        data-testid="SearchBar-rent"
                                        onClick={() => setSearchedOption("rent")}
                                        className="w-full h-full flex justify-center items-center">
                                            Rent
                                    </Link>
                                </li>
                                <li
                                    className={`min-w-[78px] rounded-tr-xl hover:opacity-80
                                        ${searchedOption === "share"
                                            ? "bg-cyan-300 text-black" : ""
                                        }
                                    `}
                                >
                                    <Link
                                        href=""
                                        data-testid="SearchBar-share"
                                        onClick={() => setSearchedOption("share")}
                                        className="w-full h-full flex justify-center items-center"
                                    >
                                            Share
                                    </Link>
                                </li>
                            </ul>
                        </div>
                    )
                }
                {/* Search form */}
                <form
                    id={`SearchBar-form-${id}`}
                    data-testid="SearchBar-form"
                    onSubmit={handleSubmit(onSubmit)}
                    className={
                        `${pathname === "/" ?   
                            "w-full py-6 px-5 md:px-14 lg:px-0 bg-blue-950 flex \
                            flex-col lg:flex-row justify-between items-end h-fit \
                            rounded-tl-none rounded-xl"
                        :   "w-full px-4 md:px-20 lg:px-10 py-4 bg-blue-950 flex \
                            flex-col lg:flex-row justify-between items-center h-fit \
                            border-t-[1px] border-solid border-blue-800 shadow-bottom shadow-gray-400"
                    }`}
                >
                    {
                        // Search options select element for pages that are not home page.
                        pathname != "/" && (
                            <div className="mb-5 lg:mb-0 w-fit">
                                <Select
                                    register={register}
                                    name="available_for"
                                    id={`available-for-${id}`}
                                    dataTestId="SearchBar-available_for"
                                    options={["sale", "rent", "share", "short_let", "lease"]}
                                    disabled={false}
                                />
                            </div>
                        )
                    }
                    {/* Container for state and city select elements */}
                    <div
                        className={`
                            ${pathname === "/" ?
                                "w-full flex mb-5 lg:mb-0 justify-between lg:justify-evenly"
                            :   "w-full lg:w-[30%] flex mb-5 lg:mb-0 justify-between lg:justify-evenly"
                            }
                        `}
                    >
                        <div className="flex flex-col w-[49%] lg:w-[43%] lg:max-w-72">
                            {
                                pathname === "/" && (
                                    <label
                                        htmlFor={`state-${id}`}
                                        className="text-white font-medium"
                                    >
                                            State
                                    </label>
                                )
                            }
                            <Select
                                register={register}
                                name="state"
                                id={`state-${id}`}
                                dataTestId="SearchBar-state"
                                options={states}
                                disabled={false}
                            />
                        </div>
                        <div className="flex flex-col w-[49%] lg:w-[43%] lg:max-w-72">
                            {
                                pathname === "/" && (
                                    <label
                                        htmlFor={`city-${id}`}
                                        className="text-white font-medium"
                                    >
                                            City
                                    </label>
                                )
                            }
                            <Select
                                register={register}
                                name="city"
                                id={`city-${id}`}
                                dataTestId="SearchBar-city"
                                options={cities}
                                disabled={!selectedState}
                            />
                        </div>
                    </div>
                    {/* Container for max and min price select elements */}
                    <div
                        className={`
                            ${pathname === "/" ?
                                "w-full flex mb-5 lg:mb-0 justify-between lg:justify-evenly"
                            :   "w-full lg:w-[30%] flex mb-5 lg:mb-0 justify-between lg:justify-evenly"
                        }`}
                    >
                        <div className="flex flex-col w-[49%] lg:w-[43%] lg:max-w-72">
                            {
                                pathname === "/" && (
                                    <label
                                        htmlFor={`min-price-${id}`}
                                        className="text-white font-medium"
                                    >
                                            Price from
                                    </label>
                                )
                            }
                            <Select
                                register={register}
                                name="min_price"
                                id={`min_price-${id}`}
                                dataTestId="SearchBar-min_price"
                                options={priceRange}
                                disabled={false}
                            />
                        </div>
                        <div
                            className="flex flex-col w-[49%] lg:w-[43%] lg:max-w-72"
                        >
                            {
                                pathname === "/" && (
                                    <label
                                        htmlFor={`max-price-${id}`}
                                        className="text-white font-medium"
                                    >
                                            Price to
                                    </label>
                                )
                            }
                            <Select
                                register={register}
                                name="max_price"
                                id={`max_price-${id}`}
                                dataTestId="SearchBar-max_price"
                                options={priceRange}
                            />
                        </div>
                    </div>
                    {/* Container for more filters and search buttons */}
                    <div
                        className={`
                            ${pathname === "/" ?
                                "w-full lg:justify-evenly flex mt-2 justify-between"
                            :   "w-full lg:w-[20%] lg:justify-between flex justify-between"
                        }`}
                    >
                        <button
                            id={`more-filters-${id}`}
                            data-testid="SearchBar-more-filters"
                            name="more filters"
                            onClick={handleMoreFilterClick}
                            type="button"
                            className={`
                                ${pathname === "/" ?
                                    "w-[49%] lg:w-[43%] lg:max-w-72 lg:min-w-24"
                                :   "w-[49%] lg:w-[47%] lg:max-w-72 lg:min-w-24"
                            }`}
                        >
                            <div
                                className={`
                                    ${pathname === "/" ?
                                        "h-8 sm:h-10 w-full rounded-lg bg-white \
                                        flex justify-center items-center hover:opacity-80"
                                    :   "h-8 sm:h-9 w-full rounded-md bg-gray-200 \
                                        flex justify-center items-center hover:opacity-80"
                                }`}
                            >
                                <span> More filters </span>
                            </div>
                        </button>
                        <div
                            className={`
                                ${pathname === "/" ?
                                    "w-[49%] lg:w-[43%] lg:max-w-72"
                                :   "w-[49%] lg:w-[47%] lg:max-w-72"
                            }`}
                        >
                            <button
                                id={`submit-${id}`}
                                data-testid="SearchBar-submit"
                                name="submit"
                                type="submit"
                                className={`
                                    ${pathname === "/" ?
                                        "h-8 sm:h-10 w-[100%] rounded-lg \
                                        bg-cyan-300 font-semibold hover:opacity-85 \
                                        flex items-center justify-center"
                                    :   "h-8 sm:h-9 w-[100%] rounded-md text-white \
                                        bg-blue-500 font-medium hover:opacity-85 \
                                        flex items-center justify-center"
                                }`}
                            >
                               <Search
                                    className="inline-block w-5 mr-1"
                                />
                                    Search
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default SearchBar;

// const { mutateAsync } = useMutation<ServerApartmentData[], Error, SearchFormData>({
//     mutationFn: async (data: SearchFormData): Promise<ServerApartmentData[]> => {
//       const response = await axiosInstance.post<ServerApartmentData[]>("api/apartments/search", data);
//       return response.data
//     }
// });

// const defaultValues = {
//     state: "",
//     city: "",
//     school: "",
//     listing_type: "",
//     max_price: 0,
//     min_price: 0,
//     amenities: []
// }

// const {
//     handleSubmit,
//     register,
//     control
//     } = useSubmitForm<SearchFormData, ServerApartmentData[]>({
//     mutateAsync,
//     defaultValues,
// })
