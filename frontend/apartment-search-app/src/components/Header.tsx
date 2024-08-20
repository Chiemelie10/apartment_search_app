import HambugerMenu from "./HambugerMenu"
import HeaderNavbar from "./HeaderNavbar";

const Header = () => {
    return (
        <header
            className="h-16 bg-blue-950 w-full flex items-center px-4
                lg:px-10 text-base"
        >
            <HambugerMenu />
            <div
                className="h-full flex items-center justify-center sm:justify-between w-full"
            >
                <span className="text-yellow-400">PropertySolutions</span>
                <HeaderNavbar />
            </div>
        </header>
    )
}

export default Header;
