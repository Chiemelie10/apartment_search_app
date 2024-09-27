"use client"

import { ReactNode, createContext, useState } from "react";


const DetailedApartmentContext = createContext<DetailedApartmentContextProps | undefined>(undefined);

export const DetailedApartmentContextProvider = ({ children } : { children : ReactNode }) => {
    const [isSharing, setIsSharing] = useState(false);
    const [apartment, setApartment] = useState<ServerApartmentData | {}>({});
    const [isSendingMessage, setIsSendingMessage] = useState(false);

    // interestsIsOpen and idealMatchIsOpen are states used in the user profile section.
    const [interestsIsOpen, setInterestsIsOpen] = useState(false);
    const [idealMatchIsOpen, setIdealMatchIsOpen] = useState(false);

    return (
        <DetailedApartmentContext.Provider
            value={{
                isSharing,
                setIsSharing,
                apartment,
                setApartment,
                isSendingMessage,
                setIsSendingMessage,
                interestsIsOpen,
                setInterestsIsOpen,
                idealMatchIsOpen,
                setIdealMatchIsOpen
            }}
        >
            { children }
        </DetailedApartmentContext.Provider>
    )
}

export default DetailedApartmentContext;
