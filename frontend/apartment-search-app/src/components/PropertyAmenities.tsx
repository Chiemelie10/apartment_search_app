"use client";

import BedIcon from "../../public/images/bedroom_icon.svg";
import BathtubIcon from "../../public/images/bathtub_icon.svg";
import GarageIcon from "../../public/images/garage_icon.svg";
import SwimmingPoolIcon from "../../public/images/swimming_pool_icon.svg";
import ToiletIcon from "../../public/images/toilet_icon.svg";
import MicrowaveIcon from "../../public/images/kitchen_microwave_icon.svg";
import building from "../../public/images/old-building-icon.svg";
import pets from "../../public/images/pets-icon.svg";
import noPets from "../../public/images/no-pets-icon.svg";
import balcony from "../../public/images/balcony-window-icon.svg";
import { capitalize } from "@/utils";
import { usePathname } from "next/navigation";


const PropertyAmenities = ({amenities}: PropertyAmenitiesProp) => {
    const pathname = usePathname();

    const amenityIcons: Record<AmenityName, any> = {
        bedroom: BedIcon,
        bathroom: BathtubIcon,
        garage: GarageIcon,
        kitchen: MicrowaveIcon,
        "swimming pool": SwimmingPoolIcon,
        toilet: ToiletIcon,
        "new building": building,
        "old building": building,
        furnished: building,
        balcony: balcony,
        veranda: balcony,
        "pets allowed": pets,
        "pets not allowed": noPets,
        none: ""
    }

    return (
        <div
            className={
                `flex text-base w-full
                ${
                    pathname?.includes("/apartments") ? "grid md:grid-cols-3 xs:grid-cols-2 grid-cols-1 gap-4"
                        :   "flex-row overflow-x-scroll py-1 border-y-[1px] \
                            border-y-solid border-y-gray-300"
                }`
            }
        >
            {amenities
                .filter(({ quantity }) => quantity > 0)
                .map(({ quantity, amenity }) => {
                    const AmenityIcon = amenityIcons[amenity.name];
                    return (
                        <div
                            key={amenity.id}
                            className={
                                `flex shrink-0
                                ${pathname?.includes("/apartments")
                                    ?   "flex-row items-center w-full"
                                    :   "flex-col w-[33.3%] xs:w-[25%]"
                                }`
                            }
                        >
                            <div className="flex items-center">
                                <AmenityIcon className="h-10 w-10"
                                />
                                {
                                    amenity.name === "swimming pool"
                                        && <span className="ml-1"> { quantity } </span>
                                }
                                {
                                    amenity.name === "bathroom"
                                        && <span className="ml-1"> { quantity } </span>
                                }
                                {
                                    amenity.name === "bedroom"
                                        && <span className="ml-1"> { quantity } </span>
                                }
                                {
                                    amenity.name === "kitchen"
                                        && <span className="ml-1"> { quantity } </span>
                                }
                                {
                                    amenity.name === "toilet"
                                        && <span className="ml-1"> { quantity } </span>
                                }
                            </div>
                            <span
                                className={
                                    `${
                                        pathname?.includes("/apartments") &&
                                            amenity.name === "garage" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "veranda" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "balcony" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "new building" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "old building" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "furnished" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "pets allowed" ? "ml-1"
                                            :   pathname?.includes("/apartments") &&
                                                amenity.name === "pets not allowed" ? "ml-1"
                                            :   pathname?.includes("/apartments") ? "ml-[0.4rem]"
                                        : ""
                                    }`
                                }
                            >
                                { amenity.name === "bedroom" && quantity <= 1 ? "Bed"
                                    : amenity.name === "bedroom" && quantity > 1 ? "Beds"
                                    : amenity.name === "bathroom" && quantity <= 1  ? "Bath"
                                    : amenity.name === "bathroom" && quantity > 1 ? "Baths"
                                    : amenity.name === "toilet" && quantity <= 1  ? "Toilet"
                                    : amenity.name === "toilet" && quantity > 1 ? "Toilets"
                                    : amenity.name === "kitchen" && quantity <= 1  ? "Kitchen"
                                    : amenity.name === "kitchen" && quantity > 1 ? "Kitchens"
                                    : amenity.name === "swimming pool"
                                        && pathname?.includes("/apartments")
                                        && quantity <= 1 ? "Swimming pool"
                                    : amenity.name === "swimming pool"
                                        && pathname?.includes("/apartments")
                                        && quantity > 1 ? "Swimming pools"
                                    : amenity.name === "swimming pool"
                                        && !pathname?.includes("/apartments")
                                        ? "PL"
                                    : capitalize(amenity.name)
                                }
                            </span>
                        </div>
                    );
                })
            }
        </div>
    );
}

export default PropertyAmenities;
