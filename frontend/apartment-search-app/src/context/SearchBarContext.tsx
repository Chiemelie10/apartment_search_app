"use client";

import { ReactNode, createContext, useState } from "react";


const SearchBarContext = createContext<SearchBarContextType | undefined>(undefined);

export const SearchBarContextProvider = ({children} : {children: ReactNode}) => {
    const [moreFilters, setMoreFilters] = useState(false);
    const [searchedOption, setSearchedOption] = useState("rent");
    const [sortType, setSortType] = useState("");


    return (
        <SearchBarContext.Provider value={{
                moreFilters, setMoreFilters, searchedOption, setSearchedOption,
                sortType, setSortType
            }}
        >
            {children}
        </SearchBarContext.Provider>
    )
}

export default SearchBarContext;
