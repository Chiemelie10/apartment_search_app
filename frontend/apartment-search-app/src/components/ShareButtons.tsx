"use client"

import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import {
    FacebookShare,
    TwitterShare,
    LinkedinShare,
    WhatsappShare,
    TelegramShare,
    EmailShare,
    VKShareShare,
    LineShare,
    RedditShare,
    TumblrShare,
    ViberShare
} from "react-share-lite";
import Overlay from "./Overlay";
import useDetailedApartmentContext from "@/hooks/useDetailedApartmentContext";
import { usePathname } from "next/navigation";

const ShareButtons = ({ title }: ShareButtonsProps) => {
    const pathname = usePathname();
    const [url, setUrl] = useState("");
    const { isSharing, setIsSharing } = useDetailedApartmentContext();

    useEffect(() => {
        if (typeof window !== "undefined" && pathname) {
            const url = `${window.location.protocol}//${window.location.host}${pathname}`;
            setUrl(url);
        }
    }, [pathname])

    const removeShareButtons = () => {
        // Hides the share buttons
        setIsSharing(false);
        document.body.style.overflow = "auto";
    }

    const shareButtons = [
        <FacebookShare url={url} quote={title} blankTarget={true} />,
        <TwitterShare url={url} title={title} blankTarget={true}/>,
        <WhatsappShare url={url} title={title} blankTarget={true}/>,
        <TelegramShare url={url} blankTarget={true}/>,
        <LinkedinShare url={url} blankTarget={true}/>,
        <EmailShare url={url} subject={title} blankTarget={true} />,
        <RedditShare url={url} blankTarget={true} />,
        <VKShareShare url={url} blankTarget={true} />,
        <LineShare url={url} blankTarget={true} />,
        <TumblrShare url={url} caption={title} blankTarget={true} />,
        <ViberShare url={url} title={title} blankTarget={true} />
    ]

    return (
        <>
            {
                isSharing && (
                    <>
                        {/* Overlay when pop up message form is active */}
                        <Overlay removeOverlay={removeShareButtons} />
                        <ul className="grid grid-cols-3 lg:grid-cols-4 gap-y-5 gap-x-5
                            w-[90%] mini:w-[73.5%] xs:w-[46%] lg:w-[35%] max-w-[30rem] h-fit p-5
                            bg-white z-20 fixed inset-0 inset-x-1/2 inset-y-1/2 transform
                            -translate-x-1/2 -translate-y-1/2 rounded-lg"
                        >
                            {shareButtons.map((shareButton, index) => {
                                return (
                                    <li
                                        key={index}
                                        className="flex justify-center items-center"
                                    >
                                        {shareButton}
                                    </li>
                                )
                            })}
                        </ul>
                    </>
                )
            }
        </>
    )
}

export default ShareButtons;
