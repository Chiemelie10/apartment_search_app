import BedIcon from "../../public/images/bedroom_icon.svg";
import BathtubIcon from "../../public/images/bathtub_icon.svg";
import GarageIcon from "../../public/images/garage_icon.svg";
import SwimmingPoolIcon from "../../public/images/swimming_pool_icon.svg";
import ToiletIcon from "../../public/images/toilet_icon.svg";
import MicrowaveIcon from "../../public/images/kitchen_microwave_icon.svg";
import { capitalize } from "@/utils";


const PropertyAmenities = ({amenities}: PropertyAmenitiesProp) => {

    const amenityIcons: Record<AmenityName, any> = {
        bedroom: BedIcon,
        bathroom: BathtubIcon,
        garage: GarageIcon,
        kitchen: MicrowaveIcon,
        "swimming pool": SwimmingPoolIcon,
        toilet: ToiletIcon,
        none: ""
    }

    return (
        <div
            className="flex text-base w-full overflow-x-scroll
                py-1 border-y-[1px] border-y-solid border-y-gray-300"
        >
            {amenities
                .filter(({ quantity }) => quantity > 0)
                .map(({ quantity, amenity }) => {
                    const AmenityIcon = amenityIcons[amenity.name];
                    return (
                        <div
                            key={amenity.id}
                            className="flex flex-col w-[33.3%] xs:w-[25%] shrink-0"
                        >
                            <div className="flex">
                                <AmenityIcon className="h-7 w-7" />
                                <span
                                    className="ml-2"
                                >
                                    { amenity.name === "garage" ? "" : quantity }
                                </span>
                            </div>
                            <span
                                className="text-sm">
                                    { amenity.name === "bedroom" ? "Beds"
                                        : amenity.name === "bathroom" ? "Baths"
                                        : amenity.name === "swimming pool" ? "PL"
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
