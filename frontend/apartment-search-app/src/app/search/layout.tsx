import { SearchBarContextProvider } from "@/context/SearchBarContext";
import { ReactNode } from "react";

const SearchLayout = ({children}: {children: ReactNode}) => {
    return (
        <SearchBarContextProvider>
            <main>{children}</main>
        </SearchBarContextProvider>
    )
}

export default SearchLayout;
