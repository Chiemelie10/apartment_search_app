"use client";

import SidebarContext from "@/context/SidebarContext"
import { useContext } from "react"

const useSidebarContext = () => {
    const sidebarContext = useContext(SidebarContext);

    if (sidebarContext === undefined) {
        throw new Error("useSidebarContext must be used with SidebarContext.")
    }

    return sidebarContext;
}

export default useSidebarContext;
