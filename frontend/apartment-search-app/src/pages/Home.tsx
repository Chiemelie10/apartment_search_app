"use client";

import Image from "next/image";
import livingRoomImage from "../../public/images/one-bedroom-apartment.jpg";
import usePaginatedProperty from "@/hooks/usePaginatedProperty";
import SearchBar from "@/components/SearchBar";
import Spinner from "@/components/Spinner";
import Link from "next/link";
import NonPaginatedProperty from "@/components/NonPaginatedProperty";
import { useQuery } from "@tanstack/react-query";
import axiosInstance from "@/api/axios";
import useSearchBarContext from "@/hooks/useSearchBarContext";
import Modal from "@/components/Modal";
import useSearchBar from "@/hooks/useSearbarBar";


const Home = () => {
    const queryKey1 = "featuredProperty";
    const url = `/apartments/featured?page=1&size=3`;

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
        data: FeaturedAparmentData,
        error,
        isError,
        isSuccess,
        isLoading
    } = usePaginatedProperty({page: 1, queryKey1, url});

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
        priceRange: searchBarPriceRange,
        id: searchBarId,
        onSubmit: searchBarOnSubmit,
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
        id: modalId,
        onSubmit: modalOnSubmit
    } = useSearchBar({ statesData });


    return (
    <>
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
                    selectedSearchBarSearchedOption={searchedOption} //Used state value
                    priceRange={modalPriceRange}
                    register={modalRegister}
                />
            )
        }
        <section className="z-10 h-fit">
            <div className="relative w-full h-64 lg:h-96">
                <Image
                    src={livingRoomImage}
                    alt=""
                    fill
                    placeholder="blur"
                    priority
                    sizes="100vw"
                    style={{objectFit: "cover"}}
                />
                <div className="absolute top-20 lg:top-36 w-full h-96 z-10">
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
                </div>
            </div>
        </section>
        <section
            className="relative h-fit pt-[270px] sm:pt-[290px] lg:pt-20 pb-16 bg-blue-200 z-0"
        >
            {isLoading && (
                <div className="h-60 flex justify-center mt-5">
                    <Spinner />
                </div>
            )}
            {FeaturedAparmentData && FeaturedAparmentData.next_page && (
                <Link
                    href="/apartments/featured"
                    className="hidden lg:inline-block"
                >
                    <span
                        className="text-gray-950 text-base absolute
                            bottom-4 right-10"
                    >
                        See more
                    </span>
                </Link>
            )}
            <NonPaginatedProperty
                data={FeaturedAparmentData}
                isSuccess={isSuccess}
                singularHeader="Featured property"
                pluralHeader="Featured properties"
            />
        </section>
    </>
        // <section>
        //     <div>
        //         <span>Find a new tenant or housemate for free</span>
        //         <span>
        //             Looking for the perfect next tenant or housemate with interests that matches yours? List your property now and connect with potential tenants easily.
        //         </span>
        //         <button>List your property now</button>
        //     </div>
        //     <div></div>
        // </section>
    // </main>
    //     <section className="mt-auto">
    //         <Footer />
    //     </section>
    // </div>
    )
}

export default Home;
