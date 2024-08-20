import Link from "next/link";
import { navBarMenuItems, services } from "@/utils";
import DesktopDropdown from "./DesktopDropdown";


const HeaderNavbar = () => {
    return (
        <div className="hidden sm:flex justify-between w-full text-base">
            <nav className="flex items-center">
                <div aria-label="properties" className="pl-8 flex">
                    {navBarMenuItems.map((item, index) => {
                        return (
                            <div key={index}>
                                {item.hasOwnProperty("children") ? (
                                    <DesktopDropdown item={item} />
                                ) : item.title === "Services" ? (
                                    <span
                                        className="text-yellow-400 mr-4 py-1 px-2 rounded-sm hidden
                                            lg:inline-block"
                                    >
                                        {item.title}
                                    </span>
                                ) : (
                                    <Link
                                        className="text-white mr-4 py-1 px-2 rounded-sm hidden
                                            lg:inline-block hover:bg-slate-500"
                                        href={item?.route || ""}
                                    >
                                        {item.title}
                                    </Link>
                                )}
                            </div>
                        )
                    })}
                </div>

                <span className="text-gray-300 mr-4 hidden lg:inline-block">Services</span>

                <div
                    aria-label="services"
                    className="flex"
                >
                    {services.map((item, index) => {
                        return (
                            <div key={index}>
                                {item.hasOwnProperty("children") ? (
                                    <DesktopDropdown item={item} />
                                ) : (
                                    <button
                                        className="text-white py-1 px-2 rounded-sm
                                            hover:text-gray-400 mr-4"
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
            <nav aria-label="auth" >
                <ul className="flex">
                    <li>
                        <Link
                            href=""
                            className="font-semibold bg-cyan-300 mr-4 py-1 px-2
                                    rounded-sm hidden lg:inline-block hover:opacity-90"
                        >
                            Post Property
                        </Link>
                    </li>
                    <li>
                        <Link
                            href="/register"
                            className="text-white py-1 px-2 rounded-sm hidden
                                    lg:inline-block hover:bg-slate-500"
                        >
                            Sign up
                        </Link>
                    </li>
                    <li>
                        <Link
                            href="/login"
                            className="bg-cyan-300 lg:bg-transparent lg:text-white
                                    py-1 px-2 rounded-sm hover:opacity-90 hover:md:bg-slate-500
                                    hidden sm:inline-block"
                        >
                            Sign in
                        </Link>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

export default HeaderNavbar;
