import ImageCarousel from "./ImageCarousel";
import Link from "next/link";
import { capitalize, getPages, getPaginationIndices } from "@/utils";
import GetNextOrPrevPage from "./GetNextOrPrevPage";
import { PaginatedPropertyProps, SearchFormData } from "@/interfaces";
import PropertyAmenities from "./PropertyAmenities";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import Select from "./Select";
import { useForm, useWatch } from "react-hook-form";
import { useEffect, useId } from "react";


const PaginatedProperty = (props: PaginatedPropertyProps) => {
    const {
        data, isSuccess, isPlaceholderData,
        page, setPage, limit,
        singularHeader, pluralHeader
    } = props;

    const pathname = usePathname();
    const router = useRouter();
    const searchParams = useSearchParams();

    const {register, control} = useForm<SearchFormData>({
        defaultValues: {
            sort_type: ""
        }
    })

    let selectedSortType = useWatch({control, name: "sort_type"});


    useEffect(() => {
        if (selectedSortType) {
            const searchedOption = searchParams?.get("available_for");


            if (selectedSortType === "Lowest price") {
                selectedSortType = "price"
            } else if (selectedSortType === "Highest price") {
                selectedSortType = "-price"
            } else if (selectedSortType === "Least recent") {
                selectedSortType = "created_at"
            } else if (selectedSortType === "Most recent") {
                selectedSortType = "-created_at"
            } else if (selectedSortType === "Least number of bedrooms") {
                selectedSortType = "bedroom"
            } else if (selectedSortType === "Most number of bedrooms") {
                selectedSortType = "-bedroom"
            }

            const params = new URLSearchParams(searchParams?.toString());
            params.set("sort_type", selectedSortType)

            const sortQueryString = params.toString()
            if (setPage) setPage(1);
            router.push(`/search/${searchedOption}?${sortQueryString}`);
        }
    }, [selectedSortType, router])

    const id = useId();


    if (isSuccess && data && data.apartments.length > 0) {
        const [start, end] = getPaginationIndices(limit, page, data);

        return (
            <div className="w-[90%] lg:w-[80%] font-serif text-base">
                {
                    data.apartments.length > 0 && (
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
                {start !== end
                ?   <div
                        className={
                            `flex flex-col gap-5 md:gap-0 md:flex-row md:justify-between
                            md:items-center
                            ${pathname === "/" ? "lg:px-10" : "lg:px-6 mt-1 md:mt-5"}`
                        }
                    >
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
                        <div>
                            <form className="flex items-center">
                                <span className="mr-2 font-bold">Sort:</span>
                                <div className="w-fit">
                                    <Select
                                        name="sort_type"
                                        register={register}
                                        id={`sort-type-${id}`}
                                        options={[
                                            "Lowest price",
                                            "Highest price",
                                            "Least recent",
                                            "Most recent",
                                            "Least number of bedrooms",
                                            "Most number of bedrooms"
                                        ]}
                                    />
                                </div>
                            </form>
                        </div>
                    </div>
                :   <div
                        className={
                            `flex flex-col gap-5 md:gap-0 md:flex-row md:justify-between
                            md:items-center
                            ${pathname === "/" ? "lg:px-10" : "lg:px-6 mt-1 md:mt-5"}`
                        }
                    >
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
                        <div>
                            <form className="flex items-center">
                                <span className="mr-2 font-bold">Sort:</span>
                                <div className="w-fit">
                                    <Select
                                        name="sort_type"
                                        register={register}
                                        id={`sort-type-${id}`}
                                        options={[
                                            "Lowest price",
                                            "Highest price",
                                            "Least recent",
                                            "Most recent",
                                            "Least number of bedrooms",
                                            "Most number of bedrooms"
                                        ]}
                                    />
                                </div>
                            </form>
                        </div>
                    </div>
                }
                <div className="w-full lg:px-6 mt-5 lg:mt-8">
                    <ul className="w-full grid grid-cols-1
                            gap-14"
                    >
                        {data?.apartments?.map((apartment) => (
                            <Link
                                href={`/apartment/${apartment.id}`}
                                key={apartment.id}
                                className="inline-block"
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
                                        <p className="mt-4 font-bold">
                                            <span>
                                                NGN {apartment.price} {
                                                    apartment.available_for === "sale" ? ""
                                                        : `/ ${apartment.price_duration}`
                                                }
                                            </span>
                                        </p>
                                        <p>{ apartment.id }</p>
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
                <GetNextOrPrevPage
                    data={data}
                    isPlaceholderData={isPlaceholderData}
                    page={page}
                    limit={limit}
                    setPage={setPage}
                />
            </div>
        )
    }

    return <></>
}

export default PaginatedProperty;
