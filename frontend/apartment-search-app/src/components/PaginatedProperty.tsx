import ImageCarousel from "./ImageCarousel";
import Link from "next/link";
import { capitalize, getPaginationIndices } from "@/utils";
import GetNextOrPrevPage from "./GetNextOrPrevPage";
import PropertyAmenities from "./PropertyAmenities";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import Select from "./Select";
import { useForm, useWatch } from "react-hook-form";
import { useEffect, useId } from "react";
import useSearchBarContext from "@/hooks/useSearchBarContext";


const PaginatedProperty = (props: PaginatedPropertyProps) => {
    const {
        data, isSuccess, isPlaceholderData,
        page, setPage, limit,
        singularHeader, pluralHeader
    } = props;


    const pathname = usePathname();
    const router = useRouter();
    const searchParams = useSearchParams();
    const { setSortType } = useSearchBarContext();

    const {register, control} = useForm<SearchFormData>({
        defaultValues: {
            sort_type: ""
        }
    })

    // uswWatch triggers rerender any time the state of sort_type select element changes.
    // It returns the latest value (string) of the current state of the element. 
    let selectedSortType = useWatch({control, name: "sort_type"});


    useEffect(() => {
        if (selectedSortType) {
            // Returns the value of available_for from the url query string.
            // available_for has values like rent, share, sale/buy, which
            // is included in the pathname of the route for searching.
            const searchedOption = searchParams?.get("available_for");

            // Adds sort_type parameter to the query string.
            const params = new URLSearchParams(searchParams?.toString());
            params.set("sort_type", selectedSortType)

            // Converts params from object to string
            const sortQueryString = params.toString()

            // Update the sortType state which is added to the query string on any form submission.
            setSortType(selectedSortType);

            /*
                Resets the page state to 1. If not done page maintains the current state
                after the sort has been done.
            */
            if (setPage) {
                setPage(1);
            }

            /*
                router.push() navigates to a new route if for example searchedOption
                was changed from rent to buy.
                It remains in the same route if only query string changes.
                The key thing is it trigers the re-render of the search results page
                which results in fresh request to the API using useQuery and axios.
            */
            router.push(`/search/${searchedOption}?${sortQueryString}`);
        }
    }, [selectedSortType, router])

    const id = useId();


    if (isSuccess && data && data.apartments.length > 0) {
        const [start, end] = getPaginationIndices(limit, page, data);

        return (
            <div
                className="w-[90%] lg:w-[80%] text-base"
            >
                {
                    data.apartments.length > 0 && (
                        // Heading for the page
                        <h1
                            className={
                                `${pathname === "/" ? "lg:px-10" : "lg:px-6 mt-5"}
                                font-bold text-lg sm:text-xl lg:text-2xl
                                text-gray-950`
                            }
                        >
                            {data.apartments.length === 1
                                ? singularHeader : pluralHeader
                            }
                        </h1>
                    )
                }
                {/* Number of displayed apartments and sort form */}
                <div
                    className={
                        `flex flex-col gap-5 md:gap-0 md:flex-row md:justify-between
                        md:items-center
                        ${pathname === "/" ? "lg:px-10" : "lg:px-6 mt-1 md:mt-5"}`
                    }
                >
                    {start !== end
                    ?
                        <div>
                            <span
                                className="text-gray-700 dark:text-gray-400"
                            >
                                Showing <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >{start} </span>to
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                > {end}</span> of <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >{data.total_number_of_apartments}</span> properties
                            </span>
                        </div>
                    :
                        <div>
                            <span
                                className="text-gray-700 dark:text-gray-400"
                            >
                                Showing <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >{start} </span>of
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                > {data.total_number_of_apartments}</span> properties
                            </span>
                        </div>
                    }
                    <div>
                        {/* Sort form */}
                        <form
                            id={`PaginatedProperty-sort-form-${id}`}
                            data-testid="PaginatedProperty-sort-form"
                            className="flex items-center"
                        >
                            <span className="mr-2 font-bold">Sort:</span>
                            <div className="w-fit">
                                <Select
                                    name="sort_type"
                                    register={register}
                                    id={`sort-type-${id}`}
                                    dataTestId="paginated-property-sort-type"
                                    options={[
                                        "price",
                                        "-price",
                                        "created_at",
                                        "-created_at",
                                        "bedroom",
                                        "-bedroom"
                                    ]}
                                />
                            </div>
                        </form>
                    </div>
                </div>
                {/* Paginated card section */}
                <div className="w-full lg:px-6 mt-5 lg:mt-8">
                    <ul className="w-full grid grid-cols-1
                            gap-14"
                    >
                        {data?.apartments?.map((apartment) => (
                            <Link
                                href={`/apartment/${apartment.id}`}
                                key={apartment.id}
                                className="inline-block"
                                data-testid={`${apartment.id}`}
                                id={`${apartment.id}`}
                            >
                                <li
                                    className="
                                        px-4 py-6 bg-white rounded-xl shadow-gray-400
                                        shadow-[0_0_7px_rgba(0,0,0,0.12)]
                                        hover:shadow-gray-400 hover:shadow-[0px_0px_13px_rgba(0,0,0,0.12)]
                                        sm:flex sm:justify-between
                                    "
                                >
                                    <div className="w-[100%] sm:w-[40%] lg:w-[31%]">
                                        <ImageCarousel images={apartment.images} />
                                    </div>
                                    <div className="w-[100%] sm:w-[57%] lg:w-[67%]">
                                        <p className="mt-0 font-semibold">
                                            {capitalize(apartment.title)}
                                        </p>
                                        <p className="mb-2 text-sm">
                                            <span>{capitalize(apartment.city.name)}, </span>
                                            <span>{capitalize(apartment.state.name)}</span>
                                        </p>
                                        <p>{apartment.listing_type}</p>
                                        <p>{apartment.floor_number}</p>
                                        <p className="mt-4 font-bold">
                                            <span>
                                                NGN {apartment.price} {
                                                    apartment.available_for === "sale" ? ""
                                                        : `/ ${apartment.price_duration}`
                                                }
                                            </span>
                                        </p>
                                        {
                                            apartment.amenities.length > 0 && (
                                                <div className="mt-4">
                                                    <PropertyAmenities amenities={apartment.amenities}/>
                                                </div>
                                            )
                                        }
                                    </div>
                                </li>
                            </Link>
                        ))}
                    </ul>
                </div>
                {/* Pagination next, previous and page buttons */}
                <GetNextOrPrevPage
                    data={data}
                    isPlaceholderData={isPlaceholderData}
                    page={page}
                    setPage={setPage}
                />
            </div>
        )
    }

    if (isSuccess && data && data.apartments.length === 0) {
        return (
            <p className="text-base">
                Sorry, no properties match your search criteria. Please try adjusting your
                filters or check back later for new listings.
            </p>
        )
    }
}

export default PaginatedProperty;
