"use client"

import { getListingType, getPriceRange } from "@/utils";
import { usePathname, useRouter } from "next/navigation";
import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import useSearchBarContext from "./useSearchBarContext";
import qs from "qs";
import { useEffect, useId } from "react";


const useSearchBar = ({ statesData, setPage }: useSearchBarProps) => {
    const router = useRouter();
    const { searchedOption, moreFilters, sortType, setMoreFilters } = useSearchBarContext();

    const pathname = usePathname();
    const id = useId();

    const {
        register,
        handleSubmit,
        reset,
        setValue,
        control
    } = useForm<SearchFormData>({
        defaultValues: {
            available_for: "",
            state: "",
            city: "",
            school: "",
            listing_type: "",
            max_price: "",
            min_price: "",
            max_room: "",
            min_room: "",
            max_floor_num: "",
            min_floor_num: "",
            amenities: []
        }
    });

    const selectedState = useWatch({control, name: "state"});
    const selectedCity = useWatch({control, name: "city"});
    const selectedMinPrice = useWatch({control, name: "min_price"});
    const selectedMaxPrice = useWatch({control, name: "max_price"});
    const selectedSearchOption = useWatch({control, name: "available_for"});

    const priceRange = getPriceRange(0, 10000000, 200000);
    const listingType = getListingType();

    // const selectedState = useWatch({control, name: "state"});
    // const selectedCity = useWatch({control, name: "city"});
    // const selectedMinPrice = useWatch({control, name: "min_price"});

    /*
        The map function is used to loop over the data returned from the API above
        to get name and id of each state object.
    */
    const states = statesData?.map((state) => ({name: state.name, id: state.id}));

    /*
        The below code uses the find function to get an array containing state objects
        that the state id matches the value returned by useWatch. In this case only one object
        will be in the array since id is unique. The map function is then used to loop
        over the cities array in the state object, returning an array of objects containing
        the name and id of each city.
    */
    const cities = selectedState
        ? statesData?.find((state) => state.id === selectedState)?.cities.map(
            (city) => ({name: city.name, id: city.id})) || []
        : [];

    // Manually sets city to empty string when state is not selected or is empty string.
    useEffect(() => {
        if (!selectedState) {
            setValue("city", "");
        }
    }, [selectedState, setValue])


    // const schools = selectedCity
    //     ? data?.find((state) => state.name === selectedState)?.cities.find(
    //         (city) => city.name === selectedCity)?.schools.map(
    //             (school) =>({name: school.name, id: school.id})) || []
    //     : [];

    // The onSubmit function only runs when the search button of the form clicked.
    const onSubmit: SubmitHandler<SearchFormData> = (formData) => {

        if (pathname === "/") {
            /*
                Assigned the value of searchOption to available_for as searchedOption is
                a constant and can't be changed or manipulated.
            */
            let available_for = searchedOption;

            /*
                available_for is added to the formData, converted to string and used to construct the
                pathname and query string passed to router.push()
            */
            if (searchedOption == "" || searchedOption == "sale" || searchedOption == "rent"
                || searchedOption == "share" || searchedOption == "short_let" || searchedOption == "lease") {
                    formData.available_for = searchedOption;
                }

            let queryString = qs.stringify(formData);

            // Add sort type selected by user to formData
            if (sortType) {
                queryString = `${queryString}&sort_type=${sortType}`
            }

            // Changed the value from sale to buy to match the route pathname "/search/buy?..."
            if (available_for === "sale") {
                available_for = "buy";
            }

            if (moreFilters) {
                setMoreFilters(false);
                document.body.style.overflow = "auto";
            }

            router.push(`/search/${available_for}?${queryString}`);
        } else  {
            /*
                This block of code runs in pages that uses the SearchBar component
                except the home page. Unlike in the block above, the value of available_for
                is not gotten from the state, searchedOption. This is because there is a
                select element with that name included in the form when SearchBar component is used
                in pages that are not the home page. The purpose of the if and else if blocks
                are to covert values of available_for from the form to the appropriate values
                that matches the expected search routes.
                Note that "searchedOption" in this block is not the one declared for state at the
                beginning of the component.
            */

            let available_for = formData.available_for
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

            // Converts the object "formData" to string 
            let queryString = qs.stringify(formData);

            // Add sort type selected by user to formData
            if (sortType) {
                queryString = `${queryString}&sort_type=${sortType}`
            }

            /*
                Resets the page state to 1. If not done page maintains the current state
                after the search button has been clicked and new page rendered. It
                ensures API request for page 1 is always made.
            */
            if (setPage) {
                setPage(1)
            }

            if (moreFilters) {
                setMoreFilters(false);
                document.body.style.overflow = "auto";
            }

            router.push(`/search/${searchedOption}?${queryString}`);
        }
    }

    return {
        states, cities, selectedState, priceRange, listingType, reset,
        id, onSubmit, setValue, handleSubmit, register, selectedCity,
        selectedMaxPrice, selectedMinPrice, selectedSearchOption, sortType
    }
}

export default useSearchBar;