import { DropdownProps } from "@/interfaces";
import { useEffect, useState } from "react";
import Link from "next/link";
import { ChevronUp, ChevronDown } from "react-feather"


const MobileDropdown = (props: DropdownProps) => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const { item, isOpen } = props;
    const menuItems = item?.children ? item.children : [];

    const toggle = () => {
        setIsDropdownOpen((prevState) => !prevState);
    }

    useEffect(() => {
        if (isOpen === false) setIsDropdownOpen(false);
    }, [isOpen])

    const transClass = isDropdownOpen ? "flex" : "hidden";

    return (
        <>
            <div className="text-base font-serif">
                <button
                    onClick={toggle}
                    className="hover:bg-gray-400 w-full hover:rounded-md"
                >
                    <div
                        className="flex items-center justify-between
                            py-1 px-2"
                    >
                        <span
                            className="text-white"
                        >
                            {item.title}
                        </span>
                        {isDropdownOpen ? <ChevronUp /> : <ChevronDown />}
                    </div>
                </button>
                <div
                    className={
                        `z-30 min-w-[200px] xs:min-w-[250px] h-fit flex flex-col py-4
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
            {isDropdownOpen ?
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

export default MobileDropdown;
