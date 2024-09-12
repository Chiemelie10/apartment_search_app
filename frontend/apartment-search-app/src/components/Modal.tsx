import useSearchBarContext from "@/hooks/useSearchBarContext";
import Input from "./Input"
import Select from "./Select"
import useSearchBar from "@/hooks/useSearbarBar";
// import { useRouter } from "next/navigation";
import { Search } from "react-feather";
import { getFloorNumbers, getListingType } from "@/utils";
import { useEffect } from "react";
import { X } from "react-feather";


const Modal = (props: ModalProps) => {
    const {
        moreFilters,
        setMoreFilters,
        handleSubmit,
        register,
        setValue,
        reset,
        states,
        cities,
        selectedState,
        selectedSearchBarState,
        selectedSearchBarCity,
        selectedSearchBarMinPrice,
        selectedSearchBarMaxPrice,
        selectedSearchBarSearchedOption,
        priceRange,
        id,
        onSubmit
    } = props;

    useEffect(() => {
        setValue("state", selectedSearchBarState)
    }, [selectedSearchBarState, setValue])

    useEffect(() => {
        setValue("city", selectedSearchBarCity)
    }, [selectedSearchBarCity, setValue])

    useEffect(() => {
        setValue("min_price", selectedSearchBarMinPrice)
    }, [selectedSearchBarMinPrice, setValue])

    useEffect(() => {
        setValue("max_price", selectedSearchBarMaxPrice)
    }, [selectedSearchBarMaxPrice, setValue])

    useEffect(() => {
        if (selectedSearchBarSearchedOption == "" || selectedSearchBarSearchedOption == "sale"
            || selectedSearchBarSearchedOption == "rent" || selectedSearchBarSearchedOption == "share"
            || selectedSearchBarSearchedOption == "short_let"
            || selectedSearchBarSearchedOption == "lease") {
                setValue("available_for", selectedSearchBarSearchedOption)
        }
    }, [selectedSearchBarSearchedOption, setValue])

    const handleMoreFilterClick = () => {
        setMoreFilters(false);
        document.body.style.overflow = "auto";
    }

    const handleReset = () => {
        reset();
    }

    const listingType = getListingType();
    const floorNumbers = getFloorNumbers();


    return (
        <>
            {
                // Overlay when pop up form is active
                moreFilters && (
                    <>
                        <div
                            onClick={handleMoreFilterClick}
                            className={
                                `w-full min-h-screen fixed inset-0 bg-black
                                bg-opacity-50 hidden md:block z-20`
                            }
                        ></div>

                        {/* Pop up search form */}
                        <div
                            className="w-[100%] md:w-[690px] h-full md:h-[90%] bg-white z-20
                                fixed inset-0 md:inset-x-1/2 md:inset-y-1/2 md:transform
                                md:-translate-x-1/2 md:-translate-y-1/2 md:rounded-lg"
                        >
                            <form
                                id={`SearchBar-form-${id}`}
                                data-testid="SearchBar-form"
                                onSubmit={handleSubmit(onSubmit)}
                                className={
                                    `relative h-full w-full`
                                }
                            >
                                {/* Form heading */}
                                <div
                                    className="h-[9%] border-b-[1px] border-b-gray-300 border-solid
                                        px-5 flex items-center justify-between md:rounded-t-lg"
                                >
                                    <div className="flex gap-7 items-center h-fit">
                                        <h2 className="font-bold text-lg">
                                            More Filters
                                        </h2>
                                        <button
                                            onClick={handleReset}
                                            type="button"
                                        >
                                            <span
                                                className="text-blue-800 text-xs mt-[3.3px]"
                                            >
                                                Reset all filters
                                            </span>
                                        </button>
                                    </div>
                                    <button
                                        onClick={handleMoreFilterClick}
                                    >
                                        <X />
                                    </button>
                                </div>
                                <div className="h-[79%] w-full pt-5 pl-5 pr-1 overflow-auto">
                                    <div className="flex flex-col mb-5">
                                        <label
                                            htmlFor={`available-for-${id}`}
                                            className="font-bold">
                                                Search options
                                        </label>
                                        <Select
                                            register={register}
                                            name="available_for"
                                            id={`available-for-${id}`}
                                            dataTestId="SearchBar-available_for"
                                            options={["sale", "rent", "share", "short_let", "lease"]}
                                            disabled={false}
                                            style={{height: "3rem", backgroundColor: "white"}}
                                            firstOptionLabel="Any"
                                        />
                                    </div>
                                    {/* Container for state, city, price and room number */}
                                    <div className="grid grid-cols-2 gap-x-6 gap-y-5 mb-5">
                                        <div className="flex flex-col">
                                            <label
                                                htmlFor={`state-${id}`}
                                                className="font-bold">
                                                    State
                                            </label>
                                            <Select
                                                register={register}
                                                name="state"
                                                id={`state-${id}`}
                                                dataTestId="SearchBar-state"
                                                options={states}
                                                disabled={false}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                        <div className="flex flex-col">
                                            <label
                                                htmlFor={`city-${id}`}
                                                className="font-bold">
                                                    City
                                            </label>
                                            <Select
                                                register={register}
                                                name="city"
                                                id={`city-${id}`}
                                                dataTestId="SearchBar-city"
                                                options={cities}
                                                disabled={!selectedState}
                                                firstOptionLabel="Any"
                                                style={{
                                                    height: "3rem",
                                                    backgroundColor: selectedState ? "white" : "#e2e8f0"
                                                }}
                                            />
                                        </div>
                                        <div className="flex flex-col">
                                            <label
                                                htmlFor={`min-price-${id}`}
                                                className="font-bold">
                                                    Price from
                                            </label>
                                            <Select
                                                register={register}
                                                name="min_price"
                                                id={`min_price-${id}`}
                                                dataTestId="SearchBar-min_price"
                                                options={priceRange}
                                                disabled={false}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                        <div
                                            className="flex flex-col"
                                        >
                                            <label
                                                htmlFor={`max-price-${id}`}
                                                className="font-bold">
                                                    Price to
                                            </label>
                                            <Select
                                                register={register}
                                                name="max_price"
                                                id={`max_price-${id}`}
                                                dataTestId="SearchBar-max_price"
                                                options={priceRange}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                        <div
                                            className="flex flex-col"
                                        >
                                            <label
                                                htmlFor={`min_room-${id}`}
                                                className="font-bold">
                                                    Rooms from
                                            </label>
                                            <Select
                                                register={register}
                                                name="min_room"
                                                id={`min_room-${id}`}
                                                dataTestId="SearchBar-min_room"
                                                options={[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                        <div
                                            className="flex flex-col"
                                        >
                                            <label
                                                htmlFor={`max_room-${id}`}
                                                className="font-bold">
                                                    Rooms to
                                            </label>
                                            <Select
                                                register={register}
                                                name="max_room"
                                                id={`max_room-${id}`}
                                                dataTestId="SearchBar-max_room"
                                                options={[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                        <div className="flex flex-col">
                                            <label
                                                htmlFor={`min_floor_num-${id}`}
                                                className="font-bold">
                                                    Floor from
                                            </label>
                                            <Select
                                                register={register}
                                                name="min_floor_num"
                                                id={`min_floor_num-${id}`}
                                                dataTestId="SearchBar-min_floor_num"
                                                options={floorNumbers}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                        <div className="flex flex-col">
                                            <label
                                                htmlFor={`max_floor_num-${id}`}
                                                className="font-bold">
                                                    Floor to
                                            </label>
                                            <Select
                                                register={register}
                                                name="max_floor_num"
                                                id={`max_floor_num-${id}`}
                                                dataTestId="SearchBar-max_floor_num"
                                                options={floorNumbers}
                                                style={{height: "3rem", backgroundColor: "white"}}
                                                firstOptionLabel="Any"
                                            />
                                        </div>
                                    </div>
                                    <div className="flex flex-col mb-5">
                                        <label
                                            htmlFor={`listing-type-${id}`}
                                            className="font-bold">
                                                Listing type
                                        </label>
                                        <Select
                                            register={register}
                                            name="listing_type"
                                            id={`listing-type-${id}`}
                                            dataTestId="SearchBar-listing_type"
                                            options={listingType}
                                            style={{height: "3rem", backgroundColor: "white"}}
                                            firstOptionLabel="Any"
                                        />
                                    </div>
                                    {/* Features and Amenities container */}
                                    <h2 className="mb-5 font-bold">Features and amenities</h2>
                                    <div className="grid grid-cols-2 gap-x-6 gap-y-5 mb-5">
                                        <div>
                                            <Input
                                                id={`bedroom-${id}`}
                                                dataTestId="SearchBar-bedroom"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Bedroom"
                                            />
                                            <label
                                                htmlFor={`bedroom-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Bedroom
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`kitchen-${id}`}
                                                dataTestId="SearchBar-kitchen"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Kitchen"
                                            />
                                            <label
                                                htmlFor={`kitchen-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Kitchen
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`toilet-${id}`}
                                                dataTestId="SearchBar-toilet"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Toilet"
                                            />
                                            <label
                                                htmlFor={`toilet-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Toilet
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`bathroom-${id}`}
                                                dataTestId="SearchBar-bathroom"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Bathroom"
                                            />
                                            <label
                                                htmlFor={`bathroom-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Bathroom
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`garage-${id}`}
                                                dataTestId="SearchBar-garage"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Garage"
                                            />
                                            <label
                                                htmlFor={`garage-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Garage
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`swimming_pool-${id}`}
                                                dataTestId="SearchBar-swimming_pool"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Swimming pool"
                                            />
                                            <label
                                                htmlFor={`swimming_pool-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Swimming pool
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`balcony-${id}`}
                                                dataTestId="SearchBar-balcony"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Balcony"
                                            />
                                            <label
                                            htmlFor={`balcony-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Balcony
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`veranda-${id}`}
                                                dataTestId="SearchBar-veranda"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Veranda"
                                            />
                                            <label
                                                htmlFor={`veranda-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Veranda
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`pets_allowed-${id}`}
                                                dataTestId="SearchBar-pets_allowed"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Pets allowed"
                                            />
                                            <label
                                                htmlFor={`pets_allowed-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Pets allowed
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`pets_not_allowed-${id}`}
                                                dataTestId="SearchBar-pets_not_allowed"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Pets not allowed"
                                            />
                                            <label
                                                htmlFor={`pets_not_allowed-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Pets not allowed
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`furnished-${id}`}
                                                dataTestId="SearchBar-furnished"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Furnished"
                                            />
                                            <label
                                                htmlFor={`furnished-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Furnished
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`elevator-${id}`}
                                                dataTestId="SearchBar-elevator"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Elevator"
                                            />
                                            <label
                                                htmlFor={`elevator-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Elevator
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`new_building-${id}`}
                                                dataTestId="SearchBar-new_building"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="New building"
                                            />
                                            <label
                                                htmlFor={`new_building-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    New building
                                            </label>
                                        </div>
                                        <div>
                                            <Input<SearchFormData>
                                                id={`old_building-${id}`}
                                                dataTestId="SearchBar-old_building"
                                                register={register}
                                                name="amenities"
                                                type="checkbox"
                                                value="Old building"
                                            />
                                            <label
                                                htmlFor={`old_building-${id}`}
                                                className="ml-3 hover:cursor-pointer">
                                                    Old building
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                {/* Submit button container */}
                                <div
                                    className="h-[12%] w-[100%] flex justify-center items-center
                                        px-5 border-t-[1px] border-t-gray-400 border-solid
                                        rounded-b-lg"
                                >
                                    <button
                                        id={`submit-${id}`}
                                        data-testid="SearchBar-submit"
                                        name="submit"
                                        type="submit"
                                        className={`
                                            h-[63%] w-[100%] rounded-xl text-white
                                            bg-blue-950 font-medium hover:bg-[#0B1A35]
                                            flex items-center justify-center`
                                        }
                                    >
                                        <Search className="inline-block w-5 mr-1"/> Search
                                    </button>
                                </div>
                            </form>
                        </div>
                    </>
                )  
            }
        </>
    )
}

export default Modal;
