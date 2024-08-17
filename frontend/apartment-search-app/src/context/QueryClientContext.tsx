"use client";

import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import { ReactNode } from "react";

// Create a client.
export const queryClient = new QueryClient();

const CustomQueryClientProvider = ({children}: {children: ReactNode}) => {
    return (
        <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    )
}

export default CustomQueryClientProvider;