import { Dispatch, RefObject, SetStateAction } from "react";
import { UseMutateAsyncFunction } from "@tanstack/react-query";
import { AxiosError } from "axios";
import {
    SubmitHandler, FieldValues, UseFormRegister, DeepMap,
    FieldErrors, DeepPartial, UseFormHandleSubmit, Control, Path, UseFormSetValue, UseFormReset,
} from "react-hook-form";

declare global {
    // Start of utils types

    type FloorNumberData = {
        id: number;
        name: string;
    }

    // End of utils types

    // start of context types
    
    type SidebarContextType = {
        isOpen: boolean;
        setIsOpen: Dispatch<SetStateAction<boolean>>;
    }

    type SearchBarContextType = {
        moreFilters: boolean;
        setMoreFilters: Dispatch<SetStateAction<boolean>>;
        searchedOption: string;
        setSearchedOption: Dispatch<SetStateAction<string>>;
        sortType: string;
        setSortType: Dispatch<SetStateAction<string>>;
    }
    
    // End of context types
    
    // start of useSubmitForm interfaces

    type UseSubmitFormProps<TFormData, TResponse> = {
        mutateAsync: UseMutateAsyncFunction<TResponse, Error, TFormData, unknown>;
        defaultValues: TFormData;
        pathname: string | null;
        query: string | null;
    }

    type UseSubmitFormReturn<TFormData extends FieldValues> = {
        register: UseFormRegister<TFormData>;
        onSubmit: SubmitHandler<TFormData>;
        handleSubmit: UseFormHandleSubmit<TFormData, undefined>;
        control: Control<TFormData>;
        errors: FieldErrors<TFormData>;
        isSubmitting: boolean;
        dirtyFields: Partial<Readonly<DeepMap<DeepPartial<TFormData>, boolean>>>;
    }
    
    type ErrorResponse = {
        [key: string]: string | string[];
    }
    
    // End of useSubmitForm interfaces
    
    // Custom axios error
    interface SearchFormValidationError extends AxiosError {
        data: SearchFormData;
    }
    
    // mutateAsync function of useMutation
    // type MutateAsync = {
    //     mutateAsync: UseMutateAsyncFunction<ServerApartmentData[], Error, SearchFormData, unknown>
    // }
    
    // Search form data type
    
    type SearchFormAmenityData = "Bedroom" | "Kitchen" | "Toilet" | "Bathroom" | "Garage"
        | "Swimming pool" | "Furnished" | "Balcony" | "Veranda" | "Pets allowed"
        | "Pets not allowed" | "Elavator" | "New building" | "Old building"

    type SearchFormData = {
        available_for: "sale" | "rent" | "share" | "short_let" | "lease" | "";
        state: string;
        city: string;
        school: string;
        listing_type: string;
        max_price: number | string;
        min_price: number | string;
        max_room: number | string;
        min_room: number | string;
        max_floor_num: number | string;
        min_floor_num: number | string;
        floor: "Groud floor" | "Not ground floor" | "";
        amenities: SearchFormAmenityData[];
        sort_type: string;
    }
    
    // End of form data type
    
    // start of Apartment and User data type from server
    
    type UserInterest = {
        id: string;
        name: string;
    }
    
    type Interest = {
        id: string;
        user_profile: string;
        user_interest: UserInterest;
    }
    
    type UserProfile = {
        gender?: string;
        phone_number?: string;
        phone_number_is_verified?: boolean;
        interests?: Interest[];
        thumbnail?: string;
        remove_thumbnail?: boolean;
        first_name?: string;
        last_name?: string;
        email?: string;
    }
    
    type User = {
        id?: string;
        username?: string;
        email?: string;
        profile_information?: UserProfile;
        last_login?: Date;
        is_active?: boolean;
        is_staff?: boolean;
        is_superuser?: boolean;
        is_verified?: boolean;
        created_at?: Date;
        updated_at?: Date;
    }
    
    type AmenityName = "bedroom" | "bathroom" | "kitchen" | "swimming pool" | "toilet"
        | "garage" | "none" | "pets allowed" | "pets not allowed" | "new building"
        | "old building" | "balcony" | "veranda";
    
    type Amenity = {
        id: string;
        name: AmenityName;
        created_at: Date;
        updated_at: Date;
    }
    
    type ServerApartmentAmenityData = {
        id: string;
        apartment: string;
        quantity: number;
        created_at: Date;
        updated_at: Date;
        amenity: Amenity;
    }
    
    type ServerApartmentImageData = {
        id: string;
        image: string;
        created_at: Date;
        updated_at: Date;
        apartment: string;
    }
    
    type ServerApartmentData = {
        id: string;
        user: User;
        country: {
            id: string;
            name: string;
        };
        state: {
            id: string;
            name: string;
            country: string;
        };
        city: {
            id: string;
            name: string;
            state: string;
        };
        school: {
            id: string;
            name: string;
            country: string;
            state: string;
            city: string;
        };
        amenities: ServerApartmentAmenityData[];
        nearest_bus_stop: string;
        listing_type: string;
        floor_number: number;
        title: string;
        description: string;
        price: number;
        price_duration: string;
        available_for: string;
        is_taken?: boolean;
        is_taken_time?: Date;
        is_taken_number?: number;
        approval_status?: string;
        images: ServerApartmentImageData[];
        video_link: string;
        advert_days_left?: number;
        advert_exp_time?: Date;
        num_of_exp_time_extension?: number;
    }

    type ApartmentData = {
        total_number_of_apartments: number;
        total_pages: number;
        previous_page: number | null;
        current_page: number;
        next_page: number | null;
        apartments: ServerApartmentData[];
    }
    
    // End of Apartment and User data from server.
    
    // Start of State, City and School data from server.
    
    type School = {
        id: string;
        name: string;
        country: string;
        state: string;
        city: string;
    }
    
    type City = {
        id: string;
        state: string;
        name: string;
        schools: School[];
    }
    
    type State = {
        id: string;
        name: string;
        country: string;
        cities: City[];
    }
    
    // End of Countries, states, cities and schools data
    
    // Start of components type
    type ButtonStyle<T> = {
        [key: string]: T;
    }
    
    type ButtonProps = {
        type: "submit" | "reset" | "button";
        label: string;
        style?: ButtonStyle<string>;
    }
    
    type ImageCarouselProp = {
        images: ServerApartmentImageData[];
    }
    
    type PropertyAmenitiesProp = {
        amenities: ServerApartmentAmenityData[];
    }
    
    type SearchBarProps = {
        setMoreFilters: Dispatch<SetStateAction<boolean>>;
        handleSubmit: UseFormHandleSubmit<SearchFormData, undefined>;
        register: UseFormRegister<SearchFormData>;
        onSubmit: SubmitHandler<SearchFormData>;
        setValue: UseFormSetValue<SearchFormData>;
        states: { name: string; id: string; }[] | undefined;
        cities: { name: string; id: string; }[];
        selectedState: string;
        selectedModalState: string; 
        selectedModalCity: string;
        selectedModalMinPrice: string | number;
        selectedModalMaxPrice: string | number;
        selectedModalSearchedOption: string;
        priceRange: number[];
        id: string;
        searchedOption: string;
        setSearchedOption: Dispatch<SetStateAction<string>>
    }
    
    type PaginatedPropertyProps = {
        data: ApartmentData | undefined;
        isSuccess?: boolean;
        isError?: boolean;
        error?: Error | null;
        isLoading?: boolean;
        isPlaceholderData: boolean;
        page: number;
        setPage: Dispatch<SetStateAction<number>>;
        limit: number;
        singularHeader: string;
        pluralHeader: string;
    }
    
    type GetNextOrPrevPageProps = {
        data: ApartmentData;
        isPlaceholderData: boolean;
        page: number;
        setPage: Dispatch<SetStateAction<number>>;
    }
    
    type NonPaginatedPropertyProps = {
        data: ApartmentData | undefined;
        isSuccess?: boolean;
        isError?: boolean;
        error?: Error | null;
        isLoading?: boolean;
        singularHeader: string;
        pluralHeader: string;
    }
    
    type MenuItems = {
        title: string;
        route?: string;
        children?: MenuItems[];
    }
    
    type DropdownProps = {
        item: MenuItems;
        isOpen?: boolean;
    }
    
    type SpinnerStyle<T> = {
        [key: string]: T;
    }
    
    type SpinnerProps = {
        style?: SpinnerStyle<string>;
    }

    type SelectStyle<T> = {
        [key: string]: T;
    }
    
    type SelectProps = {
        name: Path<SearchFormData>;
        register: UseFormRegister<SearchFormData>;
        id: string;
        options: { name: string, id: string }[] | number[] | string[] | FloorNumberData[] | undefined;
        disabled?: boolean;
        dataTestId: string;
        style?: SelectStyle<string>;
    }

    type InputProps = {
        type: string;
        name: Path<SearchFormData>;
        register: UseFormRegister<SearchFormData>;
        id: string;
        dataTestId: string;
        value?: string | number;
    }

    type ModalProps = {
        moreFilters: boolean;
        setMoreFilters: Dispatch<SetStateAction<boolean>>;
        handleSubmit: UseFormHandleSubmit<SearchFormData, undefined>;
        register: UseFormRegister<SearchFormData>;
        onSubmit: SubmitHandler<SearchFormData>;
        setValue: UseFormSetValue<SearchFormData>;
        reset: UseFormReset<SearchFormData>;
        states: { name: string; id: string; }[] | undefined;
        cities: { name: string; id: string; }[];
        selectedState: string;
        selectedSearchBarState: string;
        selectedSearchBarCity: string;
        selectedSearchBarMinPrice: string | number;
        selectedSearchBarMaxPrice: string | number;
        selectedSearchBarSearchedOption: string;
        priceRange: number[];
        id: string;
    }

    // End of components type
    
    // Start of hooks type
    
    type UsePaginatedPropertyProp = {
        page: number;
        queryKey1: string;
        queryKey2?: string;
        url: string;
    }

    type useSearchBarProps = {
        statesData: State[] | undefined;
        setPage?: Dispatch<SetStateAction<number>> | undefined;
    }
    
    // End of hooks type
    
    // Start of the page type

    type SearchPageProps = {
        singularHeading: string;
        pluralHeading: string;
    }

    // End of pages type
}
