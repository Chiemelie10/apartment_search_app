"use client";

import { useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight, Image as ImageIcon } from "react-feather";
import { usePathname } from "next/navigation";


const ImageCarousel = ({ images, Imageheight }: ImageCarouselProp) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const pathname = usePathname()

    const handleNext = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if (currentIndex < images.length - 1) {
            const newIndex = currentIndex + 1;
            setCurrentIndex(newIndex);
        }
    }

    const handlePrev = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if (currentIndex > 0) {
            const newIndex = currentIndex - 1;
            setCurrentIndex(newIndex);
        }
    }

    return (
        <div
            className={
                `relative text-base
                ${
                    pathname?.includes("/apartments") ? "flex justify-center" : ""
                }`
            }
        >
            <div
                className={
                    `relative rounded-xl
                    ${
                        pathname?.includes("/apartments") ? "w-full sm:w-[80%] md:w-[60%]"
                            : "w-full"
                    }
                    ${
                        pathname?.includes("/search") ? "h-[200px]"
                            : Imageheight ? Imageheight
                            : "h-[180px]"
                    }`
                }
            >
                <Image
                    src={images.length > 0 ? images[currentIndex].image : ""}
                    alt={`Thumbnail ${currentIndex + 1}`}
                    fill
                    style={{objectFit: "cover"}}
                    className="rounded-lg bg-blue-300"
                    sizes="(max-width: 640px) 100vw, (max-width: 1024) 50vw, 33vw"
                    priority
                />
            </div>
            <div
                className={
                    `px-1 w-full absolute
                    flex ${currentIndex - 1 < 0 ? "justify-end" : "justify-between"}
                    ${pathname?.includes("/apartments") ? "top-60" : "top-16"}`
                }
            >
                <button
                    onClick={handlePrev}
                    className={
                        `flex justify-center items-center h-8 w-8 rounded-full
                        shadow-gray-400 shadow-[0_0_7px_rgba(0,0,0,0.12)]
                        ${
                            currentIndex - 1 >= 0 ?
                            "bg-white hover:bg-gray-300" : "hidden"
                        }`
                    }
                >
                    <ChevronLeft />
                </button>
                <button
                    onClick={handleNext}
                    className={
                        `flex justify-center items-center h-8 w-8 rounded-full
                        shadow-gray-400 shadow-[0_0_7px_rgba(0,0,0,0.12)]
                        ${currentIndex + 1 < images.length ?
                            "bg-white hover:bg-gray-300" : "hidden"
                        }`
                    }
                >
                    <ChevronRight />
                </button>
            </div>
            <span
                className="bg-white flex justify-center items-center w-[4.5rem] h-8 p-[0.1rem]
                    absolute bottom-1 right-1 shadow-gray-400 shadow-[0_0_7px_rgba(0,0,0,0.12)]
                    text-center rounded-lg"
            >
                <ImageIcon className="mr-[0.3rem]" />
                <span>
                    {currentIndex + 1}/{images.length}
                </span>
            </span>
        </div>
    )
}

export default ImageCarousel;
