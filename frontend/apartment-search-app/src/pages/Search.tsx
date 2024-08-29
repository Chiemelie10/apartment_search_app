"use client";

import PaginatedProperty from "@/components/PaginatedProperty";
import SearchBar from "@/components/SearchBar"
import Spinner from "@/components/Spinner";
import usePaginatedProperty from "@/hooks/usePaginatedProperty";
import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import axiosInstance from "@/api/axios";
import useSearchBarContext from "@/hooks/useSearchBarContext";
import Modal from "@/components/Modal";
import useSearchBar from "@/hooks/useSearbarBar";


const Search = ({singularHeading, pluralHeading}: SearchPageProps) => {
    const [page, setPage] = useState(1);
    const [limit,] = useState(2);

    const searchParams = useSearchParams();
    const queryString = searchParams?.toString();
    const queryKey1 = `rentSearchResults${queryString}`;

    const url = (`/apartments/search?${queryString}&page=${page}&size=${limit}`);
    let {
        data: ApartmentData,
        isSuccess,
        isLoading,
        isPlaceholderData,
    } = usePaginatedProperty({page, queryKey1, url});

    /*
        Fetches the values from API used to pupulate the options of the
        select elements named state and city.
    */
    const {data: statesData} = useQuery<State[], Error>({
        queryKey: ["states"],
        queryFn: async (): Promise<State[]> => {
        const response = await axiosInstance.get<State[]>("/states/all");
        return response.data
        },
        refetchOnWindowFocus: false,
    });

    const {
        moreFilters,
        setMoreFilters,
        searchedOption,
        setSearchedOption
    } = useSearchBarContext();

    const {
        handleSubmit: searchBarHandleSubmit,
        register: searchBarRegister,
        setValue: searchBarSetValue,
        states: searchBarStates,
        cities: searchBarCities,
        selectedState: searchBarSelectedState,
        selectedCity: searchBarSelectedCity,
        selectedMaxPrice: searchBarSelectedMaxPrice,
        selectedMinPrice: searchBarSelectedMinPrice,
        selectedSearchOption: searchBarSelectedSearchOption,
        priceRange: searchBarPriceRange,
        sortType: searchbarSortType,
        id: searchBarId,
        onSubmit: searchBarOnSubmit
    } = useSearchBar({ statesData });

    const {
        handleSubmit: modalHandleSubmit,
        register: modalRegister,
        setValue: modalSetValue,
        reset: modalReset,
        states: modalStates,
        cities: modalCities,
        selectedState: modalSelectedState,
        selectedCity: modalSelectedCity,
        selectedMaxPrice: modalSelectedMaxPrice,
        selectedMinPrice: modalSelectedMinPrice,
        selectedSearchOption: modalSelectedSearchOption,
        priceRange: modalPriceRange,
        sortType: modalSortType,
        id: modalId,
        onSubmit: modalOnSubmit
    } = useSearchBar({ statesData });


    return (
        <div>
            {
                moreFilters && (
                    <Modal
                        moreFilters={moreFilters}
                        setMoreFilters={setMoreFilters}
                        handleSubmit={modalHandleSubmit}
                        onSubmit={modalOnSubmit}
                        setValue={modalSetValue}
                        reset={modalReset}
                        states={modalStates}
                        cities={modalCities}
                        id={modalId}
                        selectedState={modalSelectedState}
                        selectedSearchBarState={searchBarSelectedState}
                        selectedSearchBarCity={searchBarSelectedCity}
                        selectedSearchBarMinPrice={searchBarSelectedMinPrice}
                        selectedSearchBarMaxPrice={searchBarSelectedMaxPrice}
                        selectedSearchBarSearchedOption={searchBarSelectedSearchOption}
                        priceRange={modalPriceRange}
                        register={modalRegister}
                    />
                )
            }
            <section>
                <SearchBar
                    setMoreFilters={setMoreFilters}
                    handleSubmit={searchBarHandleSubmit}
                    onSubmit={searchBarOnSubmit}
                    setValue={searchBarSetValue}
                    states={searchBarStates}
                    cities={searchBarCities}
                    id={searchBarId}
                    selectedState={searchBarSelectedState}
                    selectedModalState={modalSelectedState}
                    selectedModalCity={modalSelectedCity}
                    selectedModalMinPrice={modalSelectedMinPrice}
                    selectedModalMaxPrice={modalSelectedMaxPrice}
                    selectedModalSearchedOption={modalSelectedSearchOption}
                    priceRange={searchBarPriceRange}
                    register={searchBarRegister}
                    searchedOption={searchedOption}
                    setSearchedOption={setSearchedOption}
                />
            </section>
            <section className="flex justify-center mt-5">
                {isLoading && (
                    <div className="h-60 flex justify-center mt-5">
                        <Spinner />
                    </div>
                )}
                <PaginatedProperty
                    data={ApartmentData}
                    isSuccess={isSuccess}
                    singularHeader={singularHeading}
                    pluralHeader={pluralHeading}
                    isPlaceholderData={isPlaceholderData}
                    page={page}
                    setPage={setPage}
                    limit={limit}
                    searchBarSortType={searchbarSortType}
                    modalSortType={modalSortType}
                />
            </section>
        </div>
    )
}

export default Search;
