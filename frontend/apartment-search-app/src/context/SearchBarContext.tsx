"use client";

import { ReactNode, createContext, useId, useState } from "react";
import { useForm, useWatch } from "react-hook-form";


const SearchBarContext = createContext<SearchBarContextType | undefined>(undefined);

export const SearchBarContextProvider = ({children} : {children: ReactNode}) => {
    const [moreFilters, setMoreFilters] = useState(false);
    const [searchedOption, setSearchedOption] = useState("rent");


    return (
        <SearchBarContext.Provider value={{
                moreFilters, setMoreFilters, searchedOption, setSearchedOption
            }}
        >
            {children}
        </SearchBarContext.Provider>
    )
}

export default SearchBarContext;
