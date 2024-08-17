"use client";

import PaginatedProperty from "@/components/PaginatedProperty";
import SearchBar from "@/components/SearchBar"
import Spinner from "@/components/Spinner";
import usePaginatedProperty from "@/hooks/usePaginatedProperty";
import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { SearchPageProps } from "@/interfaces";


const Search = ({singularHeading, pluralHeading}: SearchPageProps) => {
    const [page, setPage] = useState(1);
    const [limit,] = useState(2);
    const searchParams = useSearchParams();
    const queryString = searchParams?.toString();
    const queryKey1 = `rentSearchResults${queryString}`;

    const url = (`/apartments/search?${queryString}&page=${page}&size=${limit}`);
    let {
        data,
        isSuccess,
        isLoading,
        isPlaceholderData,
    } = usePaginatedProperty({page, queryKey1, url});


    return (
        <div>
            <section>
                <SearchBar setPage={setPage}/>
            </section>
            <section className="flex justify-center mt-5">
                {isLoading && (
                    <div className="h-60 flex justify-center mt-5">
                        <Spinner />
                    </div>
                )}
                <PaginatedProperty
                    data={data}
                    isSuccess={isSuccess}
                    singularHeader={singularHeading}
                    pluralHeader={pluralHeading}
                    isPlaceholderData={isPlaceholderData}
                    page={page}
                    setPage={setPage}
                    limit={limit}
                />
            </section>
        </div>
    )
}

export default Search;
