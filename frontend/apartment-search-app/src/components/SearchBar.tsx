"use client";

import { SearchBarProps, SearchFormData, State } from "@/interfaces";
import Select from "./Select";
import { useId, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import axiosInstance from "@/api/axios";
import { getListingType, getPriceRange } from "@/utils";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import qs from "qs";
import Link from "next/link";
import Spinner from "./Spinner";
import { Search } from "react-feather";


const SearchBar = ({setPage}: SearchBarProps ) => {
    const [searchedOption, setSearchedOption] = useState("rent");
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const priceRange = getPriceRange(0, 10000000, 200000);
    const listingType = getListingType();

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
    const selectedSearchOption = useWatch({control, name: "available_for"});
    // const selectedCity = useWatch({control, name: "city"});
    const selectedMinPrice = useWatch({control, name: "min_price"});

    const states = data?.map((state) => ({name: state.name, id: state.id}));

    const cities = selectedState
        ? data?.find((state) => state.id === selectedState)?.cities.map(
            (city) => ({name: city.name, id: city.id})) || []
        : [];

    // const schools = selectedCity
    //     ? data?.find((state) => state.name === selectedState)?.cities.find(
    //         (city) => city.name === selectedCity)?.schools.map(
    //             (school) =>({name: school.name, id: school.id})) || []
    //     : [];

    let isSubmittingQuery = false;
    const onSubmit: SubmitHandler<SearchFormData> = (data) => {
        isSubmittingQuery = true;
        if (pathname === "/") {
            let available_for = "";

            if (searchedOption === "buy") {
                available_for = "sale";
            } else if (searchedOption === "rent") {
                available_for = "rent";
            } else if (searchedOption === "share") {
                available_for = "share";
            }

            data.available_for = available_for;
            const queryString = qs.stringify(data);
            router.push(`/search/${searchedOption}?${queryString}`);
            isSubmittingQuery = false;
        } else  {
            let searchOption = "";
            if (selectedSearchOption === "sale") {
                searchOption = "buy"
            } else if (selectedSearchOption === "rent") {
                searchOption = "rent"
            } else if (selectedSearchOption === "share") {
                searchOption = "share"
            } else if (selectedSearchOption === "lease") {
                searchOption = "lease"
            } else if (selectedSearchOption === "short_let") {
                searchOption = "short-let"
            }

            const queryString = qs.stringify(data);
            if (setPage) setPage(1);
            router.push(`/search/${searchOption}?${queryString}`);
            isSubmittingQuery = false;
        }
    }

    const id = useId();

    return (
        <div className="flex flex-col font-serif text-base">
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
// });
