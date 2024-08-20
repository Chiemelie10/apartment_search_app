"use client";

import { useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "react-feather";
import { usePathname } from "next/navigation";


const ImageCarousel = ({ images }: ImageCarouselProp) => {
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
        <div className="relative text-base">
            <div
                className={
                    `relative w-full rounded-xl
                    ${pathname?.includes("/search") ? "h-[200px]" : "h-[180px]"}`
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
            <div className="w-full px-1 flex justify-between absolute top-16">
                <button
                    onClick={handlePrev}
                    className={
                        `flex justify-center items-center h-8 w-8 rounded-full
                        ${currentIndex - 1 >= 0
                            ? "bg-white" : "bg-gray-300"}
                        ${currentIndex - 1 >= 0 ? "hover:bg-gray-300" : ""}`
                    }
                >
                    <ChevronLeft />
                </button>
                <button
                    onClick={handleNext}
                    className={
                        `flex justify-center items-center h-8 w-8 rounded-full
                        ${currentIndex + 1 < images.length
                            ? "bg-white" : "bg-gray-300"}
                        ${currentIndex + 1 < images.length ? "hover:bg-gray-300" : ""}`
                    }
                >
                    <ChevronRight />
                </button>
            </div>
            <span
                className="bg-white inline-block w-10 text-center rounded-md
                    absolute bottom-1 right-1"
            >
                {currentIndex + 1}/{images.length}
            </span>
        </div>
    )
}

export default ImageCarousel;
