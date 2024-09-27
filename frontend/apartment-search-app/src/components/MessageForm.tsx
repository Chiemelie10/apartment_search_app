import useDetailedApartmentContext from "@/hooks/useDetailedApartmentContext";
import { isServerApartmentData } from "@/utils";
import { useEffect, useId } from "react";
import { PhoneCall, X } from "react-feather";
import { SubmitHandler, useForm } from "react-hook-form";
import Link from "next/link";
import TextArea from "./TextArea";
import { capitalize } from "@/utils";
import Overlay from "./Overlay";

const MessageForm = () => {
    const { apartment, setIsSendingMessage } = useDetailedApartmentContext();
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
            {/* Overlay when pop up message form is active */}
            <div className="lg:hidden">
                <Overlay removeOverlay={closeMessageForm} />
            </div>
            <div
                className="w-[90%] xs:w-[80%] lg:w-full max-w-[30rem] lg:max-w-none
                    h-fit p-5 bg-white z-20 fixed lg:static inset-0 inset-x-1/2 inset-y-1/2
                    transform -translate-x-1/2 -translate-y-1/2 rounded-lg lg:rounded-md
                    lg:inset-auto lg:inset-x-0 lg:inset-y-0 lg:transform-none
                    lg:shadow-gray-400 lg:shadow-[0_0_7px_rgba(0,0,0,0.12)] lg:pt-2"
            >
                <form onSubmit={handleSubmit(onSubmit)}>
                    <h2
                        className="hidden lg:block text-xl font-bold text-blue-950 mb-4"
                    >
                        Contact the advertiser
                    </h2>
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
                                className="hover:cursor-pointer lg:hidden"
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
                {
                    isServerApartmentData(apartment) && apartment.user.profile_information?.phone_number && (
                        <Link
                            className="hidden w-full h-10
                            bg-blue-800 hover:bg-blue-900 mt-4 rounded-md lg:flex
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
        </>
    )
}

export default MessageForm;
