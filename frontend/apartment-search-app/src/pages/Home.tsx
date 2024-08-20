"use client";

import Image from "next/image";
import livingRoomImage from "../../public/images/one-bedroom-apartment.jpg";
import usePaginatedProperty from "@/hooks/usePaginatedProperty";
import SearchBar from "@/components/SearchBar";
import Spinner from "@/components/Spinner";
import Link from "next/link";
import NonPaginatedProperty from "@/components/NonPaginatedProperty";


const Home = () => {
    const queryKey1 = "featuredProperty";
    const url = `/apartments/featured?page=1&size=3`;
    const {
        data,
        error,
        isError,
        isSuccess,
        isLoading
    } = usePaginatedProperty({page: 1, queryKey1, url});


    return (
    // <div className="flex flex-col min-h-screen">
    //     <section>
    //         <Header />
    //     </section>
    // <main>
    <>
        <section className="z-10 h-fit">
            <div className="relative w-full h-64 lg:h-96">
                <Image
                    src={livingRoomImage}
                    alt=""
                    fill
                    placeholder="blur"
                    priority
                    sizes="100vw"
                    style={{objectFit: "cover"}}
                />
                <div className="absolute top-20 lg:top-36 w-full h-96 z-10">
                    <SearchBar />
                </div>
            </div>
        </section>
        <section
            className="relative h-fit pt-[270px] sm:pt-[290px] lg:pt-20 pb-16 bg-blue-200 z-0"
        >
            {isLoading && (
                <div className="h-60 flex justify-center mt-5">
                    <Spinner />
                </div>
            )}
            {data && data.next_page && (
                <Link
                    href="/apartments/featured"
                    className="hidden lg:inline-block"
                >
                    <span
                        className="text-gray-950 text-base absolute
                            bottom-4 right-10"
                    >
                        See more
                    </span>
                </Link>
            )}
            <NonPaginatedProperty
                data={data}
                isSuccess={isSuccess}
                singularHeader="Featured property"
                pluralHeader="Featured properties"
            />
        </section>
    </>
        // <section>
        //     <div>
        //         <span>Find a new tenant or housemate for free</span>
        //         <span>
        //             Looking for the perfect next tenant or housemate with interests that matches yours? List your property now and connect with potential tenants easily.
        //         </span>
        //         <button>List your property now</button>
        //     </div>
        //     <div></div>
        // </section>
    // </main>
    //     <section className="mt-auto">
    //         <Footer />
    //     </section>
    // </div>
    )
}

export default Home;
