// This file defines the GetNextOrPrevPage component.

import { getPages, setScrollPosition } from "@/utils";
import { useEffect, useId } from "react";
import { ArrowLeft, ArrowRight } from "react-feather";

const GetNextOrPrevPage = (props: GetNextOrPrevPageProps) => {
    /*
        This component is used to display the next, previous, and
        page number buttons at the bottom of any pagniated section.
    */
    const {data, isPlaceholderData, page, setPage} = props;

    /*
        getPages function returns the an array of page numbers.
        These numbers are used to create clickable page numbers
        for the paginated section.
    */
    const pages = getPages(page, data);

    /*
        hasMore variable is used to check if there are more page number buttons
        after the currently displayed ones.
    */
    let hasMore = false;
    const totalPages = data.total_pages;
    if (totalPages > pages[pages.length -1]) {
        hasMore = true;
    }

    const getPreviousPage = () => {
        // Sets a new page state when previous button is clicked.
        setPage((prevState) => Math.max(prevState - 1, 1));
    }

    const getNextPage = () => {
        // Sets a new page state when next button is clicked.
        if (!isPlaceholderData && data.next_page) {
            setPage((prevState) => prevState + 1);
        }
    }

    const handlePageButtonClick = (destinationPageNum: number) => {
        // Sets a new page state when a page button is clicked.
        setPage(destinationPageNum);
    }

    useEffect(() => {
        /*
            setScrollPosition function sets scroll position to the top of the page.
            The second argument "[page]" passed to useEffect ensures it only happens
            when page state changes. 
        */
        setScrollPosition();
    }, [page])

    const id = useId();

    return (
        <div className="flex items-center justify-center my-12 md:my-16">
            <button
                id={`prev-button-${id}`}
                data-testid="GetNextOrPrevPage-prev-button"
                onClick={getPreviousPage}
                disabled={page === 1}
                className={`flex items-center justify-center px-2 md:px-3 h-8 md:h-10
                    text-white bg-blue-800 rounded-s
                    ${data.previous_page ? "hover:bg-blue-900" : ""}
                    dark:bg-gray-800 
                    dark:border-gray-700 dark:text-gray-400
                    dark:hover:bg-gray-700 dark:hover:text-white
                    mr-1 md:mr-0`}
                >
                <ArrowLeft className="inline-block mini:hidden md:inline-block" /> Prev
            </button>
            <div className="md:mx-5 h-8 md:h-10 hidden mini:flex">
                {
                    pages.map((pageNumber, index) => {
                        if (pageNumber === page) {
                            return (
                                <button
                                    id={`page-button-${id}-${index}`}
                                    data-testid={`GetNextOrPrevPage-page-button-${index}`}
                                    key={index}
                                    disabled={true}
                                    className="border-blue-500 border-solid border-[1px]
                                        w-8 md:w-10 h-8 md:h-10 mx-1 md:mx-2 rounded-sm"
                                >
                                        {pageNumber}
                                </button>
                            )
                        }
                        return (
                            <button
                                id={`page-button-${id}-${index}`}
                                data-testid={`GetNextOrPrevPage-page-button-${index}`}
                                key={index}
                                onClick={() => handlePageButtonClick(pageNumber)}
                                className="w-8 md:w-10 h-8 md:h-10 mx-1 md:mx-2 bg-gray-200
                                    hover:bg-gray-300 rounded-sm border-solid border-[1px]
                                    border-gray-400"
                            >
                                    {pageNumber}
                            </button>
                        )
                    })
                }
                {
                    hasMore && (
                            <span
                                className="w-8 md:w-10 h-8 md:h-10 mx-1 md:mx-2 bg-gray-200 flex
                                    rounded-sm border-solid border-[1px] border-gray-400
                                    justify-center items-center"
                            >
                                    ...
                            </span>
                    )
                }
            </div>
            <button
                id={`next-button-${id}`}
                data-testid="GetNextOrPrevPage-next-button"
                onClick={getNextPage}
                disabled={isPlaceholderData || !data?.next_page}
                className={`flex items-center justify-center px-2 md:px-3 h-8 md:h-10
                text-white bg-blue-800 border-0 border-s border-gray-700
                rounded-e ${data.next_page ? "hover:bg-blue-900" : ""}
                dark:bg-gray-800 dark:border-gray-700
                dark:text-gray-400 dark:hover:bg-gray-700
                dark:hover:text-white ml-1 md:ml-0`}
            >
                Next <ArrowRight className="inline-block mini:hidden md:inline-block" />
            </button>
        </div>
    )
}

export default GetNextOrPrevPage;
