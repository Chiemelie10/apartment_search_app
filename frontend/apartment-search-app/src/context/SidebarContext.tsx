"use client"

import { useState, createContext, ReactNode } from "react";


const SidebarContext = createContext<SidebarContextType | undefined>(undefined);

export const SidebarProvider = ({children} : {children: ReactNode;}) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <SidebarContext.Provider value={{isOpen, setIsOpen}}>
            {children}
        </SidebarContext.Provider>
    )
}

export default SidebarContext;
