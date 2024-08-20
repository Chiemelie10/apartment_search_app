"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import MobileDropdown from "./MobileDropdown";
import {
    mobileAuthentication,
    mobileProperties,
    otherMenuItems,
    services
} from "@/utils";


const HambugerMenu = () => {
    // State of side navbar.
    const [isOpen, setIsOpen] = useState(false);
    const [hasMounted, setHasMounted] = useState(false);

    // This function opens the side navbar and disables body scrolling.
    // It is passed to the onClick event of the hamburger menu.
    const openSideNavbar = () => {
        setIsOpen(true);
        document.body.style.overflow = "hidden";
    }

    // This function closes the side navbar and allows body scrolling.
    // It is passed to the onClick event of the overlay that covers
    // the rest of the page not covered by the side navbar and the close (X)
    // button at the top of the opened side navbar.
    const closeSideNavbar = () => {
        setIsOpen(false);
        document.body.style.overflow = "auto";
    }

    // This hook sets the hasMounted state to true when this component
    // has been renderded on the webpage. It is used to regulate the
    // time it takes the side navbar to slide back into a hidden position.
    // It is set to take 0 seconds to enter a hidden state when this hook
    // has not run, this is to ensure the side navbar is not briefly seen
    // to be sliding into it's hidden position when ever the page is opened
    // or reloaded.
    useEffect(() => {
        setHasMounted(true);
    }, []);


    return (
        <>
            {/* Hamburger menu */}
            <div
                onClick={openSideNavbar}
                tabIndex={isOpen ? -1 : 0}
                className="w-6 mr-2 flex flex-col justify-center cursor-pointer lg:hidden"
            >
                <div className="bg-white w-6 h-0.5 rounded-lg"></div>
                <div className="bg-white w-6 h-0.5 rounded-lg my-1.5"></div>
                <div className="bg-white w-6 h-0.5 rounded-lg"></div>
            </div>
            {/* Overlay */}
            <div
                className={
                    `w-full min-h-screen absolute top-0 left-0 inset-0 bg-black
                    bg-opacity-50 lg:hidden transition-transform ease-in-out z-20
                    ${hasMounted ? "duration-500" : "duration-0"}
                    transform ${isOpen ? "translate-x-0" : "-translate-x-full"}`
                }
                onClick={closeSideNavbar}
            ></div>
            {/* Side NavBar */}
            <div
                className={
                    `bg-blue-950 absolute top-0 left-0 w-[90%] xs:w-[85%] sm:w-[80%] md:w-3/4 h-full
                    px-4 py-2 lg:hidden overflow-y-auto flex flex-col z-30 text-base
                    transition-transform ease-in-out ${hasMounted ? "duration-300" : "duration-0"}
                    transform ${isOpen ? "translate-x-0" : "-translate-x-full"}`
                }
            >
                {/* Menu close button */}
                <button
                    tabIndex={isOpen ? 0 : -1}
                    type="button"
                    onClick={closeSideNavbar}
                    className="text-4xl md:text-5xl self-end text-white"
                >
                    &times;
                </button>
                <nav 
                    className="mt-1 flex flex-col sm:items-center border-t-2
                        border-solid border-blue-800"
                >
                    <div className="flex justify-between min-w-[200px] xs:min-w-[250px]
                        pt-4 pb-6 xs:pb-4 mb-4 rounded-md sm:w-9/12 md:w-10/12 sm:max-w-[600px]
                        flex-col gap-3 xs:flex-row xs:gap-0 border-b-2 border-solid
                        border-blue-800"
                    >
                        {mobileAuthentication.map((item, index) => {
                            return (
                                <div key={index}>
                                    {item.hasOwnProperty("children") ? (
                                        <MobileDropdown item={item} isOpen={isOpen} />
                                    ) : item.title === "Post property" ? (
                                        <button
                                            className="text-black px-2 py-1 rounded-md
                                                bg-cyan-300 hover:opacity-85"
                                        >
                                            <Link
                                                href={item?.route || ""}
                                                tabIndex={-1}
                                            >
                                                {item.title}
                                            </Link>
                                        </button>
                                    ) : (
                                        <button
                                            className="text-white py-1 rounded-sm
                                                hover:bg-gray-400 px-2"
                                        >
                                            <Link
                                                href={item?.route || ""}
                                                tabIndex={-1}
                                            >
                                                {item.title}
                                            </Link>
                                        </button>
                                    )}
                                </div>
                            )
                        })}
                    </div>

                    <span className="my-2 md:mt-4 text-white">Available properties</span>
                    <div
                        className="min-w-[200px] xs:min-w-[250px] p-1 my-2 bg-blue-800
                            rounded-md sm:w-9/12 md:w-10/12 sm:max-w-[600px]"
                    >
                        {mobileProperties.map((item, index) => {
                            return (
                                <div key={index}>
                                    {item.hasOwnProperty("children") ? (
                                        <MobileDropdown item={item} isOpen={isOpen} />
                                    ) : (
                                        <button
                                            className="text-white py-1 px-2 rounded-md
                                                hover:bg-gray-400 w-full flex"
                                        >
                                            <Link
                                                href={item?.route || ""}
                                            >
                                                {item.title}
                                            </Link>
                                        </button>
                                    )}
                                </div>
                            )
                        })}
                    </div>

                    <span className="my-2 text-white">Services</span>

                    <div
                        className="min-w-[200px] xs:min-w-[250px] p-1 my-2 bg-blue-800 rounded-md
                            sm:w-9/12 md:w-10/12 sm:max-w-[600px]"
                    >
                        {services.map((item, index) => {
                            return (
                                <div key={index}>
                                    {item.hasOwnProperty("children") ? (
                                        <MobileDropdown item={item} isOpen={isOpen} />
                                    ) : (
                                        <button
                                            className="text-white py-1 px-2 rounded-md
                                                hover:text-gray-400 w-full flex"
                                        >
                                            <Link
                                                href={item?.route || ""}
                                                tabIndex={-1}
                                            >
                                                {item.title}
                                            </Link>
                                        </button>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                    <span className="my-2 text-white">Others</span>

                    <div
                        className="min-w-[200px] xs:min-w-[250px] p-1 my-2 bg-blue-800 rounded-md
                            sm:w-9/12 md:w-10/12 sm:max-w-[600px]"
                    >
                        {otherMenuItems.map((item, index) => {
                            return (
                                <div key={index}>
                                    {item.hasOwnProperty("children") ? (
                                        <MobileDropdown item={item} isOpen={isOpen} />
                                    ) : (
                                        <button
                                            className="text-white py-1 px-2 rounded-md
                                                hover:bg-gray-400 w-full flex"
                                        >
                                            <Link
                                                href={item?.route || ""}
                                                tabIndex={-1}
                                            >
                                                {item.title}
                                            </Link>
                                        </button>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </nav>
            </div>
        </>
    )
}

export default HambugerMenu;