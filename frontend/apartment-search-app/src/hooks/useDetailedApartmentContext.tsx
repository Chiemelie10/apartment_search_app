"use client"

import DetailedApartmentContext from "@/context/DetailedApartmentContext"
import { useContext } from "react"

const useDetailedApartmentContext = () => {
    const detailedApartmentContext = useContext(DetailedApartmentContext);

    if (detailedApartmentContext === undefined) {
        throw new Error("DetailedApartmentContext must be used with DetailedApartmentContextProvider.");
    }

    return detailedApartmentContext;
}

export default useDetailedApartmentContext;
