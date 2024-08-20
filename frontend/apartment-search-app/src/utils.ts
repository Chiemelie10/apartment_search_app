export const getPriceRange = (min: number, max: number, step: number): number[] => {
    /*
        This function returns an array of numbers utilized in the SearchBar component.
        The numbers in the array are displayed as options for the select element with
        names "min_price" and "max_price".
    */
    let prices: number[] = [];
    for (let num = min; num <= max; num += step) {
        prices.push(num);
    }
    return prices;
}

export const getListingType = (): string[] => {
    /*
        This function returns an array of listing type used in the SearchBar component.
        The items in the array are displayed as options for the select element with
        name value "listing_type".
    */
    return [
        "none self-contained",
        "self-contained",
        "flat",
        "office space",
        "bungalow",
        "duplex",
        "mansion"
    ]
}

export const capitalize = (value: string): string => {
    /*
        This function capitalizes the first character of a string.
    */
    const fisrtLetter = value.charAt(0);
    const firstLetterCap = fisrtLetter.toUpperCase();
    const remainingLetters = value.slice(1);
    const capitalizedValue = firstLetterCap + remainingLetters;

    return capitalizedValue;
}

export const getPaginationIndices = (limit: number, page: number, data: ApartmentData) => {
    /*
        Description: This function is useful for pagination. It returns the starting
        and ending positions (type number) of Apartment objects in the data array returned
        by the API. For context, it's values was used in displaying "1 to 5 of 20 apartments."
    */
    const dataLength = data.total_number_of_apartments;
    const start = (page - 1) * limit + 1;
    let end = page * limit;

    if (end > dataLength) {
        end = dataLength;
    }

    return [start, end]
}

export const getPages = (page: number, data: ApartmentData) => {
    /*
        This function returns an array of page numbers. The page
        numbers are displayed as clickable buttons at the bottom
        of any pagination section.
    */
    const totalPages = data.total_pages;

    const pages: number[] = []
    let count = 1

    if (page === 1) {
        for (let i = page; i <= totalPages; i += 1) {
            if (count > 4) break;
            pages.push(i);
            count += 1;
        }
    } else if (page > 1 && totalPages <= 4) {
        for (let i = 1; i <= totalPages; i += 1) {
            if (count > 4) break;
            pages.push(i);
            count += 1;
        }
    } else if (page > 1 && totalPages > 4 && page != totalPages) {
        if (page - 2 <= 0) {
            for (let i = 1; i <= totalPages; i += 1) {
                if (count > 4) break;
                pages.push(i);
                count += 1;
            }
        } else if (page - 2 === 1) {
            for (let i = 2; i <= totalPages; i += 1) {
                if (count > 4) break;
                pages.push(i);
                count += 1;
            }
        } else if (page - 2 > 1 && totalPages - page >= 2) {
            for (let i = page - 1; i <= totalPages; i += 1) {
                if (count > 4) break;
                pages.push(i);
                count += 1;
            }
        } else if (page - 2 > 1 && totalPages - page === 1) {
            for (let i = page - 2; i <= totalPages; i += 1) {
                if (count > 4) break;
                pages.push(i);
                count += 1;
            }
        }
    } else if (page > 1 && totalPages > 4 && page === totalPages) {
        for (let i = page - 3; i <= totalPages; i += 1) {
            if (count > 4) break;
            pages.push(i);
            count += 1;
        }
    }

    return pages;
}

export const setScrollPosition = () => {
    // This function sets scroll position the top of the page.
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    })
} 

export const otherMenuItems: MenuItems[] = [
    {
        title: "About us",
        route: "/register"
    },
    {
        title: "Contact us",
        route: ""
    },
]

export const mobileAuthentication: MenuItems[] = [
    {
        title: "Sign up",
        route: "/register"
    },
    {
        title: "Sign in",
        route: "/login"
    },
    {
        title: "Post property",
        route: ""
    },
]

export const services: MenuItems[] = [
    {
        title: "Agents",
        route: "/",
        children: [
            {
                title: "Real estate agents in Enugu",
                route: "/"
            },
            {
                title: "Real estate agents in Lagos",
                route: "/"
            },
            {
                title: "All real estate agents"
            }
        ]
    }
]

export const mobileProperties: MenuItems[] = [
    {
        title: "Buy",
        route: "/",
        children: [
            {
                title: "Flats and apartments for sale",
                route: "/"
            },
            {
                title: "Buildings for sale",
                route: "/"
            },
            {
                title: "Shops for sale",
                route: "/"
            },
            {
                title: "Lands for sale",
                route: "/"
            },
            {
                title: "All properties for sale",
                route: "/"
            }
        ]
    },
    {
        title: "Rent",
        route: "/",
        children: [
            {
                title: "Flats and apartments for rent",
                route: "/"
            },
            {
                title: "Buildings for rent",
                route: "/"
            },
            {
                title: "Shops for rent",
                route: "/"
            },
            {
                title: "Land lease",
                route: "/"
            },
            {
                title: "All properties for rent",
                route: "/"
            }
        ]
    },
    {
        title: "Share",
        route: "/",
        children: [
            {
                title: "Flats and apartments for share",
                route: "/"
            },
            {
                title: "Buildings for share",
                route: "/"
            },
            {
                title: "All properties for share",
                route: "/"
            }
        ]
    },
]


export const navBarMenuItems: MenuItems[] = [
    {
        title: "Home",
        route: "/"
    },
    {
        title: "Buy",
        route: "/",
        children: [
            {
                title: "Flats and apartments for sale",
                route: "/"
            },
            {
                title: "Buildings for sale",
                route: "/"
            },
            {
                title: "Shops for sale",
                route: "/"
            },
            {
                title: "Lands for sale",
                route: "/"
            },
            {
                title: "All properties for sale",
                route: "/"
            }
        ]
    },
    {
        title: "Rent",
        route: "/",
        children: [
            {
                title: "Flats and apartments for rent",
                route: "/"
            },
            {
                title: "Buildings for rent",
                route: "/"
            },
            {
                title: "Shops for rent",
                route: "/"
            },
            {
                title: "Land lease",
                route: "/"
            },
            {
                title: "All properties for rent",
                route: "/"
            }
        ]
    },
    {
        title: "Share",
        route: "/",
        children: [
            {
                title: "Flats and apartments for share",
                route: "/"
            },
            {
                title: "Buildings for share",
                route: "/"
            },
            {
                title: "All properties for share",
                route: "/"
            }
        ]
    },
]
