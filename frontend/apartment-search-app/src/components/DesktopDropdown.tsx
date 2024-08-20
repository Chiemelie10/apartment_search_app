"use client";

import { useState } from "react";
import Link from "next/link";


const DesktopDropdown = (props: DropdownProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const { item } = props;
    const menuItems = item?.children ? item.children : [];

    const toggle = () => {
        setIsOpen((prevState) => !prevState);
    }

    const transClass = isOpen ? "flex" : "hidden";

    return (
        <>
            <div className="relative text-base">
                <button
                    className="text-white mr-4 py-1 px-2 rounded-sm hidden
                        lg:inline-block hover:bg-slate-500"
                    onClick={toggle}
                >
                    {item.title}
                </button>
                <div
                    className={
                        `absolute top-8 z-30 min-w-[250px] h-fit flex flex-col py-4
                        bg-white rounded-md ${transClass}`
                    }
                >
                    {
                        menuItems.map((item, index) =>
                            item.title.includes("All") ? (
                                <Link
                                    key={index}
                                    href={item?.route || ""}
                                    onClick={toggle}
                                    className="hover:bg-gray-200 px-4 py-1 z-50 text-black
                                        border-t-gray-200 border-t-solid border-t-[1px] mt-1 block"
                                >
                                    {item.title}
                                </Link>
                            ) : (
                                <Link
                                    key={index}
                                    href={item?.route || ""}
                                    onClick={toggle}
                                    className="hover:bg-gray-200 px-4 py-1 z-50 text-black"
                                >
                                    {item.title}
                                </Link>
                            )
                        )
                    }
                </div>
            </div>
            {isOpen ?
                <div
                    className="fixed top-0 right-0 bottom-0 left-0 z-20 bg-transparent"
                    onClick={toggle}
                ></div>
                :
                <></>
            }
        </>
    )
}

export default DesktopDropdown;