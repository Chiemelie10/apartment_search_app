import axiosInstance from "@/api/axios";
import { keepPreviousData, useQuery } from "@tanstack/react-query";

const usePaginatedProperty = ({page, queryKey1, url}: UsePaginatedPropertyProp) => {
    const fetchFeaturedApartments = async (page = 1): Promise<ApartmentData> => {
        const response = await axiosInstance.get<ApartmentData>(url);
        return response.data;
    }

    return useQuery({
        queryKey: [queryKey1, page],
        queryFn: () => fetchFeaturedApartments(page),
        refetchOnWindowFocus: false,
        placeholderData: keepPreviousData
    });
}

export default usePaginatedProperty;
