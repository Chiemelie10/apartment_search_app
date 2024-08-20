"use client";

import Select from "./Select";
import { useId, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import axiosInstance from "@/api/axios";
import { getListingType, getPriceRange } from "@/utils";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import qs from "qs";
import Link from "next/link";
import { Search } from "react-feather";


const SearchBar = ({setPage}: SearchBarProps ) => {
    // This component displays a searchbar on pages it is used in.

    const [searchedOption, setSearchedOption] = useState("rent");
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const priceRange = getPriceRange(0, 10000000, 200000);
    const listingType = getListingType();

    /*
        Fetches the values from API used to pupulate the options of the
        select elements named state and city.
    */
    const {isError, error, data} = useQuery<State[], Error>({
        queryKey: ["states"],
        queryFn: async (): Promise<State[]> => {
        const response = await axiosInstance.get<State[]>("/states/all");
        return response.data
        },
        refetchOnWindowFocus: false,
    });

    const {
        register,
        handleSubmit,
        control,
    } = useForm<SearchFormData>({
        defaultValues: {
            available_for: "",
            state: "",
            city: "",
            school: "",
            listing_type: "",
            max_price: "",
            min_price: "",
            amenities: []
        }
    });

    const selectedState = useWatch({control, name: "state"});
    // const selectedCity = useWatch({control, name: "city"});
    const selectedMinPrice = useWatch({control, name: "min_price"});

    /*
        The map function is used to loop over the data returned from the API above
        to get name and id of each state object.
    */
    const states = data?.map((state) => ({name: state.name, id: state.id}));

    /*
        The below code uses the find function to get an array containing state objects
        that the state id matches the value returned by useWatch. In this case only one object
        will be in the array since id is unique. The map function is then used to loop
        over the cities array in the state object, returning an array of objects containing
        the name and id of each city.
    */
    const cities = selectedState
        ? data?.find((state) => state.id === selectedState)?.cities.map(
            (city) => ({name: city.name, id: city.id})) || []
        : [];

    // const schools = selectedCity
    //     ? data?.find((state) => state.name === selectedState)?.cities.find(
    //         (city) => city.name === selectedCity)?.schools.map(
    //             (school) =>({name: school.name, id: school.id})) || []
    //     : [];

    // The onSubmit function only runs when the search button of the form clicked.
    const onSubmit: SubmitHandler<SearchFormData> = (data) => {

        if (pathname === "/") {
            /*
                This block of code only runs on home page. it assigns the value of
                searchedOption state to the created variable available_for.
                available_for is the parameter name the API expects the query string to have.
                The main purpose of the if block to assign the state value "buy" as "sale" to
                available_for. The value sale is one of the values expected by the API for
                the available_for parameter not buy.
            */
            let available_for = "";

            if (searchedOption === "buy") {
                available_for = "sale";
            } else if (searchedOption === "rent") {
                available_for = "rent";
            } else if (searchedOption === "share") {
                available_for = "share";
            }

            /*
                available_for is added to the data, converted to string and used to construct the
                pathname and query string passed to router.push()
            */
            data.available_for = available_for;
            const queryString = qs.stringify(data);
            router.push(`/search/${searchedOption}?${queryString}`);
        } else  {
            /*
                This block of code runs in pages that uses the SearchBar component
                except the home page. Unlike in the block above, the value of available_for
                is not gotten from the state, searchedOption. This is because there is a
                select element with that name included in the form when SearchBar component is used
                in pages that are not the home page. The purpose of the if and else if blocks
                are to covert values of available_for, from the form, to the appropriate values
                that matches the expected search routes and assigning it to searchedOption variable.
                Note that "searchedOption" in this block is not the one declared for state at the
                beginning of the component.
            */

            const available_for = data.available_for
            let searchedOption = "";

            if (available_for === "sale") {
                searchedOption = "buy"
            } else if (available_for === "rent") {
                searchedOption = "rent"
            } else if (available_for === "share") {
                searchedOption = "share"
            } else if (available_for === "lease") {
                searchedOption = "lease"
            } else if (available_for === "short_let") {
                searchedOption = "short-let"
            }

            // Converts the object "data" to string 
            const queryString = qs.stringify(data);

            /*
                Resets the page state to 1. If not done page maintains the current state
                after the search button has been clicked and new page rendered. It
                ensures API request for page 1 is always made.
            */
            if (setPage) {
                setPage(1)
            }

            /*
                router.push() navigates to a new route if for example pathname, searchedOption,
                was changed from rent to buy in the new search.
                It remains in the same route if only query string changes.
                The key thing is it trigers the re-render of the search results page
                which results in fresh request to the API using useQuery and axios.
            */
            router.push(`/search/${searchedOption}?${queryString}`);
        }
    }

    const id = useId();

    return (
        <div className="flex flex-col text-base">
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
            <div
                className={`
                    w-full flex flex-col justify-start items-center
                    ${pathname === "/" ? "lg:px-10" : "lg:px-0"}
                `}
            >
                {
                    pathname === "/" && (
                        <div className="md:self-start h-16 bg-blue-950 rounded-t-xl
                            border-b-[1px] border-solid border-b-gray-500"
                        >
                            <ul className="flex h-full text-white divide-x divide-solid
                                divide-gray-600"
                            >
                                <li
                                    className={`min-w-[78px] rounded-tl-xl hover:opacity-80
                                        ${searchedOption === "buy"
                                            ? "bg-cyan-300 text-black" : ""
                                        }
                                    `}
                                >
                                    <Link
                                        href=""
                                        data-testid="SearchBar-buy"
                                        onClick={() => setSearchedOption("buy")}
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
                                        className="text-white font-medium">
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
                                        className="text-white font-medium">
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
                                        className="text-white font-medium">
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
                                        className="text-white font-medium">
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
                    {/* <div className="flex flex-col">
                        <label
                            htmlFor={`listing-type-${id}`}
                            className="text-white font-medium">
                                Listing type
                        </label>
                        <Select
                            register={register}
                            name="listing_type"
                            id={`listing-type-${id}`}
                            options={listingType}
                            disabled={false}
                        />
                    </div> */}
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
