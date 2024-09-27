import useDetailedApartmentContext from "@/hooks/useDetailedApartmentContext"
import { capitalize, isServerApartmentData } from "@/utils";
import Image from "next/image";
import Link from "next/link";
import { ChevronDown, ChevronUp } from "react-feather";
import MessageForm from "./MessageForm";

const ApartmentUserProfile = () => {
    const {
        apartment,
        interestsIsOpen,
        setInterestsIsOpen,
        idealMatchIsOpen,
        setIdealMatchIsOpen
    } = useDetailedApartmentContext();

    const toggleInterestsDisplay = () => {
        // This function toggles display of interest values on the web page.
        setInterestsIsOpen((prevState) => !prevState);
    }

    const toggleIdealMatchDisplay = () => {
        // This function toggles display of ideal match values on the web page.
        setIdealMatchIsOpen((prevState) => !prevState);
    }

    return (
        <>
            { isServerApartmentData(apartment) && (
                <div className="flex flex-col shadow-gray-400
                    shadow-[0_0_7px_rgba(0,0,0,0.12)] px-5 py-4 rounded-md
                    w-full md:w-[80%] lg:w-full self-center mt-10 lg:mt-0"
                >
                    <div className="flex">
                        <div className="relative h-20 w-20 bg-blue-950 rounded-md">
                            {
                                apartment.user.profile_information?.thumbnail && (
                                    <Image
                                        src={apartment.user.profile_information?.thumbnail}
                                        alt="Profile picture"
                                        fill
                                        className="rounded-md"
                                        sizes="15vw"
                                    />
                                )
                            }
                        </div>
                        <div className="ml-2">
                            <div>
                                <span className="font-medium text-blue-950">
                                    { capitalize(apartment.user.username) }
                                </span>
                            </div>
                            <Link
                                href={`/apartments/${apartment.user.id}`}
                                className="text-sm text-blue-700 mt-2 block"
                            >
                                View more listings by this user
                            </Link>
                        </div>
                    </div>
                    {
                        apartment.user.profile_information?.interests &&
                            apartment.available_for === "share" && (
                            <div className="mt-5">
                                <div className="flex justify-between items-center">
                                    <h2
                                        className="text-xl font-bold text-blue-950 mb-2
                                            hover:cursor-pointer"
                                        onClick={toggleInterestsDisplay}
                                    >
                                        My hobbies and interests
                                    </h2>
                                    {
                                        interestsIsOpen
                                            ?   <ChevronUp
                                                    stroke="#1e3a8a"
                                                    onClick={toggleInterestsDisplay}
                                                    className="hover:cursor-pointer"
                                                />
                                            :   <ChevronDown
                                                    stroke="#1e3a8a"
                                                    onClick={toggleInterestsDisplay}
                                                    className="hover:cursor-pointer"
                                                />
                                    }
                                </div>
                                <ul
                                    className={
                                        `${interestsIsOpen ? "sm:grid grid-cols-2" : "hidden"}`
                                    }
                                >
                                    {apartment.user.profile_information.interests.map((interest) => {
                                        return (
                                            <li
                                                key={interest.user_interest.id}
                                                className="list-inside list-disc text-blue-950"
                                            >
                                                <span className="text-black">
                                                    {capitalize(interest.user_interest.name)}
                                                </span>
                                            </li>
                                        )
                                    })}
                                </ul>
                            </div>
                        )
                    }
                    {
                        apartment.user_preferred_qualities &&
                            apartment.available_for === "share" && (
                            <div className="mt-5">
                                <div className="flex justify-between items-center">
                                    <h2
                                        className="text-xl font-bold text-blue-950 mb-2
                                            hover:cursor-pointer"
                                        onClick={toggleIdealMatchDisplay}
                                    >
                                        Looking for
                                    </h2>
                                    {
                                        idealMatchIsOpen
                                            ?   <ChevronUp
                                                    stroke="#1e3a8a"
                                                    onClick={toggleIdealMatchDisplay}
                                                    className="hover:cursor-pointer"
                                                />
                                            :   <ChevronDown
                                                    stroke="#1e3a8a"
                                                    onClick={toggleIdealMatchDisplay}
                                                    className="hover:cursor-pointer"
                                                />
                                    }
                                </div>
                                <ul
                                    className={
                                        `${idealMatchIsOpen ? "sm:grid grid-cols-2" : "hidden"}`
                                    }
                                >
                                    {apartment.user_preferred_qualities.map((quality) => {
                                        return (
                                            <li
                                                key={quality.user_preferred_quality.id}
                                                className="list-inside list-disc text-blue-950"
                                            >
                                                <span className="text-black">
                                                    {capitalize(quality.user_preferred_quality.name)}
                                                </span>
                                            </li>
                                        )
                                    })}
                                </ul>
                            </div>
                        )
                    }
                </div>
            )}
        </>
    )
}

export default ApartmentUserProfile;
