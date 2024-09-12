"use client";

import ImageCarousel from "@/components/ImageCarousel";
import { Heart, MapPin, Share2, X } from "react-feather";
import qs from "qs";
import { usePathname } from "next/navigation";
import { capitalize, isServerApartmentData, setScrollPosition } from "@/utils";
import PropertyAmenities from "@/components/PropertyAmenities";
import Image from "next/image";
import { SubmitHandler, useForm } from "react-hook-form";
import { useId, useEffect, useState } from "react";
import TextArea from "@/components/TextArea";
import { useQuery } from "@tanstack/react-query";
import axiosInstance from "@/api/axios";
import Link from "next/link";
import Video from "@/components/Video";
import {
    PhoneCall, ChevronUp, ChevronDown,
    Video as PlayVideoIcon, Image as ImageIcon} from "react-feather"


const Apartment = () => {
    const [apartment, setApartment] = useState<ServerApartmentData | {}>({});
    const [apartmentId, setApartmentId] = useState("");
    const [isInStorage, setIsInStorage] = useState(true);
    const [isSendingMessage, setIsSendingMessage] = useState(false);
    const [interestsIsOpen, setInterestsIsOpen] = useState(false);
    const [idealMatchIsOpen, setIdealMatchIsOpen] = useState(false);
    const [playVideo, setPlayVideo] = useState(false);
    const pathname = usePathname();

    /*
        Coverting apartment data in sessionStorage from string to object and updating
        the apartment state.
        Getting apartment Id from the pathname of the url and updating apartmentId state.
        The id is used to make API call to fetch the apartment when it is not found in
        sessionStorage.
    */
    useEffect(() => {
        const selectedApartment = sessionStorage.getItem("selectedApartment");
        if (selectedApartment) {
            setApartment(qs.parse(selectedApartment));
        } else {
            setIsInStorage(false);
        }

        if (pathname) {
            const urlPaths = pathname.split("/");
            const apartmentId = urlPaths[urlPaths.length - 1];
            setApartmentId(apartmentId);
        }
    }, [])


    /*
        Fetches the apartment using apartment id from API if type of apartment in state
        is not ServerApartment data.
    */
    const {data: fetchedApartment} = useQuery<ServerApartmentData, Error>({
        queryKey: ["apartment"],
        queryFn: async (): Promise<ServerApartmentData> => {
        const response = await axiosInstance.get<ServerApartmentData>(`/apartments/${apartmentId}`);
        return response.data
        },
        refetchOnWindowFocus: false,
        enabled: !isInStorage
    });

    /*
        Updates the apartment state with the fetched apartment data. UseEffect is necessary to
        prevent infinite loop.
    */
    useEffect(() => {
        if (fetchedApartment) {
            setApartment(fetchedApartment);
        }
    }, [fetchedApartment, setApartment])


    const {
        register,
        handleSubmit,
        reset
    } = useForm<MessageFormData>({
        defaultValues: {
            whatsappPhoneNumber: "",
            text: ""
        }
    });

    useEffect(() => {
        if (isServerApartmentData(apartment)) {
            console.log(apartment)
            reset({
                whatsappPhoneNumber: `${apartment.user.profile_information?.phone_number ? apartment.user.profile_information?.phone_number : ""}`,
                text: `Hi, I'm interested in the ${apartment.listing_type} property ${apartment.address ? `at ${apartment.address}.` : `near ${capitalize(apartment.nearest_bus_stop)}, in ${capitalize(apartment.city.name)}, ${capitalize(apartment.state.name)}.`} Could you share more details or arrange a viewing?`
            })
        }
    }, [apartment])

    const closeMessageForm = () => {
        // Useful for mobile and tablet views
        setIsSendingMessage(false);
        document.body.style.overflow = "auto";
    }

    const openMessageForm = () => {
        // Useful for mobile and tablet views
        setIsSendingMessage(true);
        document.body.style.overflow = "hidden";
    }

    const toggleInterestsDisplay = () => {
        // This function toggles display of interest values on the web page.
        setInterestsIsOpen((prevState) => !prevState);
    }

    const toggleIdealMatchDisplay = () => {
        // This function toggles display of ideal match values on the web page.
        setIdealMatchIsOpen((prevState) => !prevState);
    }

    const onVideoPlayer = () => {
        setPlayVideo(true);
        setScrollPosition();
    }

    const offVideoPlayer = () => {
        setPlayVideo(false);
        setScrollPosition();
    }

    const onSubmit: SubmitHandler<MessageFormData> = (formData) => {
        const text = formData.text;
        const phoneNumber = formData.whatsappPhoneNumber;

        if (phoneNumber) {
            window.open(`https://wa.me/${phoneNumber}?text=${text}`, "_blank");
        }
    }

    const id = useId();

    return (
        <>
            {isServerApartmentData(apartment) && (
                <div className="relative">
                    {isSendingMessage && (
                        <>
                            {/* Overlay when pop up message form is active */}
                            <div
                                onClick={closeMessageForm}
                                className={
                                    `w-full min-h-screen fixed inset-0 bg-black
                                    bg-opacity-50 z-20`
                                }
                            ></div>

                            {/* Pop up message form */}
                            <div
                                className="w-[90%] xs:w-[80%] max-w-[30rem] h-fit p-5 bg-white
                                    z-20 fixed inset-0 inset-x-1/2 inset-y-1/2 transform
                                    -translate-x-1/2 -translate-y-1/2 rounded-lg"
                            >
                                <form onSubmit={handleSubmit(onSubmit)}>
                                    <div
                                        className="flex flex-col mb-5"
                                    >
                                        <div
                                            className="flex justify-between items-center mb-4"
                                        >
                                            <label
                                                className="text-blue-950
                                                    font-bold w-fit"
                                                htmlFor={`text-${id}`}
                                            >
                                                Message
                                            </label>
                                            <X
                                                onClick={closeMessageForm}
                                                className="hover:cursor-pointer"
                                            />
                                        </div>
                                        <TextArea<MessageFormData>
                                            register={register}
                                            name="text"
                                            id={`text-${id}`}
                                            dataTestId="Apartment-text"
                                            style={{
                                                height: "8rem",
                                                width: "100%",
                                                border: "1px solid #1e3a8a",
                                                borderRadius: "0.3rem",
                                                padding: "0.5rem"
                                            }}
                                        />
                                    </div>
                                    <button
                                        className="w-full h-10 bg-[#25D366] hover:bg-green-600
                                            rounded-md flex justify-center items-center text-white"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="22" height="22" fill="white">
                                        <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                                        <span className="ml-[0.3rem]">Whatsapp</span>
                                    </button>
                                </form>
                            </div>
                        </>
                    )}
                    <div className="px-4 lg:px-10 mt-10 mb-7 text-base">
                        <h1 className="text-2xl font-bold text-blue-950">{apartment.title}</h1>
                        {/* Mobile and tablet view like and share buttons*/}
                        <div
                            className="flex flex-col fixed top-44 right-5 gap-5
                            lg:hidden z-10"
                        >
                            <div
                                className="shadow-gray-400 shadow-[0_0_7px_rgba(0,0,0,0.12)]
                                    rounded-full w-10 h-10 flex justify-center items-center
                                    hover:cursor-pointer z-10 bg-white"
                            >
                                <Heart className="h-5" stroke="#1e3a8a"/>
                            </div>
                            <div
                                className="shadow-gray-400 shadow-[0_0_7px_rgba(0,0,0,0.12)]
                                    rounded-full w-10 h-10 flex justify-center items-center
                                    hover:cursor-pointer z-10 bg-white"
                            >
                                <Share2 className="h-5" stroke="#1e3a8a"/>
                            </div>
                        </div>
                        {/* Desktop view like and share buttons */}
                        <div className="flex">
                            <div className="mt-10 flex justify-between w-full lg:w-[70%] text-blue-950">
                                <div>
                                    <span className="text-xl font-medium">Type: </span>
                                    <span>{capitalize(apartment.listing_type)}</span>
                                </div>
                                <div className="hidden lg:flex justify-end items-center">
                                    <Heart className="h-5 hover:cursor-pointer" stroke="#1e3a8a" />
                                    <span className="mx-[0.40rem]">Save</span>
                                    <Share2 className="h-5 hover:cursor-pointer" stroke="#1e3a8a" />
                                    <span className="ml-[0.40rem]">Share</span>
                                </div>
                            </div>
                            {/* The below div is just for styling purposes. */}
                            <div className="hidden lg:block ml-5 md:w-[24rem]"></div>
                        </div>
                        <div className="flex mt-6">
                            <div className="w-full lg:w-[70%] flex flex-col">
                                {/* Property images */}
                                <div className="w-full h-fit bg-gray-100">
                                    {
                                        !playVideo && (
                                            <ImageCarousel
                                                images={apartment.images}
                                                Imageheight="h-[30rem]"
                                            />
                                        )
                                    }
                                    {
                                        playVideo && (
                                            <Video
                                                src={apartment.video_link}
                                                title={apartment.title}
                                            />
                                        )
                                    }
                                </div>
                                {/* Price */}
                                <div className="mt-6 flex justify-between items-center">
                                    <span className="text-3xl text-blue-950 font-medium">
                                        &#8358; {apartment.price} / {apartment.price_duration}
                                    </span>
                                    {
                                        apartment.video_link && (
                                            <div className="flex items-center gap-2">
                                                {
                                                    !playVideo ? <PlayVideoIcon /> : <ImageIcon />
                                                }
                                                {
                                                    !playVideo
                                                        ?   (
                                                        <button onClick={onVideoPlayer}>
                                                            <span
                                                                className="text-blue-700"
                                                            >
                                                                Play video
                                                            </span>
                                                        </button>
                                                    )   :   (
                                                        <button onClick={offVideoPlayer}>
                                                            <span
                                                                className="text-blue-700"
                                                            >
                                                                View images
                                                            </span>
                                                        </button>
                                                    )
                                                }
                                            </div>
                                        )
                                    }
                                </div>
                                {/* Mobile and tablet view user profile */}
                                <div className="lg:hidden flex flex-col shadow-gray-400
                                    shadow-[0_0_7px_rgba(0,0,0,0.12)] px-5 py-4 rounded-md
                                    w-full md:w-[80%] self-center mt-10"
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
                                                        Hobbies and interests
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
                                                            >
                                                                {capitalize(interest.user_interest.name)}
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
                                                        Ideal match
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
                                                            >
                                                                {capitalize(quality.user_preferred_quality.name)}
                                                            </li>
                                                        )
                                                    })}
                                                </ul>
                                            </div>
                                        )
                                    }
                                </div>
                                <div className="mt-10">
                                    <h2
                                        className="text-xl font-bold text-blue-950 mb-4"
                                    >
                                        Description
                                    </h2>
                                    {apartment.description}
                                </div>
                                <div className="mt-10">
                                    <h2
                                        className="text-xl font-bold text-blue-950 mb-4"
                                    >
                                        Property location
                                    </h2>
                                    <div className="flex items-center">
                                        <MapPin className="h-4 w-fit mr-[0.3rem]"/>
                                        <span>
                                            {apartment.address ? `${apartment.address} state.` : `Near ${capitalize(apartment.nearest_bus_stop)}, ${capitalize(apartment.city.name)}, ${capitalize(apartment.state.name)} state.`}
                                        </span>
                                    </div>
                                </div>
                                <div className="mt-10">
                                    <h2
                                        className="text-xl font-bold text-blue-950 mb-4"
                                    >
                                        Features and amenities
                                    </h2>
                                    <PropertyAmenities amenities={apartment.amenities} />
                                </div>
                            </div>
                            {/* Desktop view user profile and contact form */}
                            <div className="hidden lg:block ml-5 md:w-[24rem]">
                                <div className="flex flex-col shadow-gray-400
                                    shadow-[0_0_7px_rgba(0,0,0,0.12)] px-5 py-4 mb-5 rounded-md"
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
                                                        Hobbies and interests
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
                                                    className={`${interestsIsOpen ? "block" : "hidden"}`}
                                                >
                                                    {apartment.user.profile_information.interests.map((interest) => {
                                                        return (
                                                            <li
                                                                key={interest.user_interest.id}
                                                            >
                                                                {capitalize(interest.user_interest.name)}
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
                                                        Ideal match
                                                    </h2>
                                                    {
                                                        idealMatchIsOpen
                                                        ?   <ChevronUp
                                                                className="hover:cursor-pointer"
                                                                stroke="#1e3a8a"
                                                                onClick={toggleIdealMatchDisplay}
                                                            />
                                                        :   <ChevronDown
                                                                className="hover:cursor-pointer"
                                                                stroke="#1e3a8a"
                                                                onClick={toggleIdealMatchDisplay}
                                                            />
                                                    }
                                                </div>
                                                <ul
                                                    className={`${idealMatchIsOpen ? "block" : "hidden"}`}
                                                >
                                                    {apartment.user_preferred_qualities.map((quality) => {
                                                        return (
                                                            <li
                                                                key={quality.user_preferred_quality.id}
                                                            >
                                                                {capitalize(quality.user_preferred_quality.name)}
                                                            </li>
                                                        )
                                                    })}
                                                </ul>
                                            </div>
                                        )
                                    }
                                </div>
                                <div
                                    className="shadow-gray-400
                                    shadow-[0_0_7px_rgba(0,0,0,0.12)] p-5 pt-2 rounded-md"
                                >
                                    <form onSubmit={handleSubmit(onSubmit)}>
                                        <h2
                                            className="text-xl font-bold text-blue-950 mb-4"
                                        >
                                            Contact the advertiser
                                        </h2>
                                        <div
                                            className="flex flex-col mb-5"
                                        >
                                            <label
                                                className="text-blue-950
                                                    font-bold mb-2 w-fit"
                                                htmlFor={`text-${id}`}
                                            >
                                                Message
                                            </label>
                                            <TextArea<MessageFormData>
                                                register={register}
                                                name="text"
                                                id={`text-${id}`}
                                                dataTestId="Apartment-text"
                                                style={{
                                                    height: "8rem",
                                                    width: "100%",
                                                    border: "1px solid #1e3a8a",
                                                    borderRadius: "0.3rem",
                                                    padding: "0.5rem"
                                                }}
                                            />
                                        </div>
                                        <button
                                            className="w-full h-10 bg-[#25D366] hover:bg-green-600
                                                rounded-md flex justify-center items-center text-white"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="22" height="22" fill="white">
                                            <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                                            <span className="ml-[0.3rem]">Whatsapp</span>
                                        </button>
                                    </form>
                                    {
                                        apartment.user.profile_information?.phone_number && (
                                            <Link
                                                className="w-full h-10
                                                bg-blue-800 hover:bg-blue-900 mt-4 rounded-md flex
                                                justify-center items-center text-white"
                                                href={`tel:${apartment.user.profile_information?.phone_number}`}
                                            >
                                                <PhoneCall
                                                    className="mr-[0.3rem] h-[45%]"
                                                />
                                                { apartment.user.profile_information?.phone_number }
                                            </Link>
                                        )
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                    {/* Tablet and mobile view user contact information */}
                    <div
                        className="sticky bottom-0 px-4 mb-5 pb-5 text-base
                            flex items-center justify-between lg:hidden"
                    >
                        {
                            apartment.user.profile_information?.phone_number && (
                                <>
                                    <Link
                                        className="w-[45%] h-10 hidden
                                        bg-blue-800 hover:bg-blue-900 rounded-md sm:flex
                                        justify-center items-center text-white"
                                        href={`tel:${apartment.user.profile_information?.phone_number}`}
                                    >
                                        <PhoneCall
                                            className="mr-[0.3rem] h-[45%] flex justify-center items-center"
                                        />
                                        { apartment.user.profile_information?.phone_number }
                                    </Link>
                                    <Link
                                        className="w-[45%] h-10 sm:hidden
                                        bg-blue-800 hover:bg-blue-900 rounded-md flex
                                        justify-center items-center text-white"
                                        href={`tel:${apartment.user.profile_information?.phone_number}`}
                                    >
                                        <PhoneCall
                                            className="mr-[0.3rem] h-[45%] flex justify-center items-center"
                                        />
                                        Call
                                    </Link>
                                </>
                            )
                        }
                        <button
                            className="w-[45%] h-10 bg-[#25D366] hover:bg-green-600
                                rounded-md flex justify-center items-center text-white"
                            onClick={openMessageForm}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="22" height="22" fill="white">
                            <path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                            <span className="ml-[0.3rem]">Whatsapp</span>
                        </button>
                    </div>
                </div>
            )}
        </>
    )
}

export default Apartment;
