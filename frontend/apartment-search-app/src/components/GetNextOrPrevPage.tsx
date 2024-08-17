import { GetNextOrPrevPageProps } from "@/interfaces";
import { getPages } from "@/utils";
import { ArrowLeft, ArrowRight } from "react-feather";

const GetNextOrPrevPage = (props: GetNextOrPrevPageProps) => {
    const {data, isPlaceholderData, limit, page, setPage} = props;

    const pages = getPages(page, data);
    const totalPages = data.total_pages;
    let hasMore = false;
    if (totalPages > pages[pages.length -1]) {
        hasMore = true;
    }


    return (
        <div className="flex items-center justify-center my-12 md:my-16">
            <button
                onClick={() => setPage((prevState) => Math.max(prevState - 1, 1))}
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
                                key={index}
                                onClick={() => setPage(pageNumber)}
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
                onClick={() => {
                    if (!isPlaceholderData && data.next_page) {
                      setPage((prevState) => prevState + 1)
                    }
                  }}
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