"use client";

import SearchBarContext from "@/context/SearchBarContext";
import { useContext } from "react";

const useSearchBarContext = () => {
    const searchBarContext = useContext(SearchBarContext);

    if (searchBarContext === undefined) {
        throw new Error("SearchBarContext must be used with SearchBarContextProvider.");
    }

    return searchBarContext;
    
}

export default useSearchBarContext;
