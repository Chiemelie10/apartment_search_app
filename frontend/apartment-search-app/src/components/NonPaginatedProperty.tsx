import ImageCarousel from "./ImageCarousel";
import Link from "next/link";
import { capitalize } from "@/utils";
import PropertyAmenities from "./PropertyAmenities";


const NonPaginatedProperty = (props: NonPaginatedPropertyProps) => {
    const { data, isSuccess, singularHeader, pluralHeader } = props;


    if (isSuccess && data && data.apartments.length > 0) {
        return (
            <div className="w-full text-base">
                <h1
                    className="px-4 lg:px-10 font-bold text-lg sm:text-xl lg:text-2xl
                        text-gray-950"
                    >
                    {data.apartments.length === 1
                        ? singularHeader : pluralHeader
                    }
                </h1>
                <div className="w-full lg:px-6 mt-5 lg:mt-8">
                    <ul
                        className="w-full flex overflow-x-auto p-4 gap-10 md:gap-9 lg:gap-10
                            lg:grid lg:grid-cols-3"
                    >
                        {data?.apartments?.map((apartment) => (
                            <Link
                                href={`/apartment/${apartment.id}`}
                                key={apartment.id}
                                className="min-w-[100%] sm:min-w-[47%] md:min-w-[47.7%]
                                    lg:min-w-[auto] inline-block"
                            >
                                <li
                                    className="
                                        px-4 py-6 bg-white rounded-xl
                                        shadow-[0_0_7px_rgba(0,0,0,0.12)]
                                        hover:shadow-gray-400 hover:shadow-[0px_0px_13px_rgba(0,0,0,0.12)]
                                    "
                                >
                                    <ImageCarousel images={apartment.images} />
                                    <p className="mt-4">
                                        
                                        {capitalize(apartment.title)}
                                    </p>
                                    <p className="mt-2 font-bold">
                                        <span>
                                            NGN {apartment.price} {
                                                apartment.available_for === "sale" ? ""
                                                    : `/ ${apartment.price_duration}`
                                            }
                                        </span>
                                    </p>
                                    <p className="mb-4 text-sm">
                                        <span>{capitalize(apartment.city.name)}, </span>
                                        <span>{capitalize(apartment.state.name)}</span>
                                    </p>
                                    <PropertyAmenities amenities={apartment.amenities}/>
                                </li>
                            </Link>
                        ))}
                    </ul>
                </div>
            </div>
        )
    }

    return ""
}

export default NonPaginatedProperty;
