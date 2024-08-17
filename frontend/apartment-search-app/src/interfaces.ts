import { Dispatch, SetStateAction } from "react";
import { QueryObserverResult, RefetchOptions, UseMutateAsyncFunction } from "@tanstack/react-query";
import { AxiosError } from "axios";
import {
    SubmitHandler, FieldValues, UseFormRegister, DeepMap,
    FieldErrors, DeepPartial, UseFormHandleSubmit, Control,
} from "react-hook-form";

// start of context types

export type SidebarContextType = {
    isOpen: boolean;
    setIsOpen: Dispatch<SetStateAction<boolean>>;
}

// End of context types

// start of useSubmitForm interfaces

export interface UseSubmitFormProps<TFormData, TResponse> {
    mutateAsync: UseMutateAsyncFunction<TResponse, Error, TFormData, unknown>;
    defaultValues: TFormData;
    pathname: string | null,
    query: string | null
}

export interface UseSubmitFormReturn<TFormData extends FieldValues> {
    register: UseFormRegister<TFormData>;
    onSubmit: SubmitHandler<TFormData>;
    handleSubmit: UseFormHandleSubmit<TFormData, undefined>;
    control: Control<TFormData>;
    errors: FieldErrors<TFormData>;
    isSubmitting: boolean;
    dirtyFields: Partial<Readonly<DeepMap<DeepPartial<TFormData>, boolean>>>;
}

export interface ErrorResponse {
    [key: string]: string | string[]
}

// End of useSubmitForm interfaces

// Custom axios error
export interface SearchFormValidationError extends AxiosError {
    data: SearchFormData
}

// mutateAsync function of useMutation
// export type MutateAsync = {
//     mutateAsync: UseMutateAsyncFunction<ServerApartmentData[], Error, SearchFormData, unknown>
// }

// Search form data type

type SearchFormAmenityData = {
    amenity: string,
    quantity: number
}

export type SearchFormData = {
    available_for: string
    state: string,
    city: string,
    school: string,
    listing_type: string,
    max_price: number | string,
    min_price: number | string,
    amenities: SearchFormAmenityData[]
    sort_type: string
}

// End of form data type

// start of Apartment and User data type from server

export type UserInterest = {
    id: string,
    name: string
}

export type Interest = {
    id: string,
    user_profile: string,
    user_interest: UserInterest
}

export type UserProfile = {
    gender?: string,
    phone_number?: string,
    phone_number_is_verified?: boolean,
    interests?: Interest[],
    thumbnail?: string,
    remove_thumbnail?: boolean,
    first_name?: string,
    last_name?: string,
    email?: string
}

export type User = {
    id?: string;
    username?: string;
    email?: string,
    profile_information?: UserProfile,
    last_login?: Date,
    is_active?: boolean,
    is_staff?: boolean,
    is_superuser?: boolean,
    is_verified?: boolean,
    created_at?: Date,
    updated_at?: Date,
}

export type AmenityName = "bedroom" | "bathroom" | "kitchen" | "swimming pool" | "toilet"
    | "garage" | "none"

type Amenity = {
    id: string,
    name: AmenityName,
    created_at: Date,
    updated_at: Date
}

type ServerApartmentAmenityData = {
    id: string,
    apartment: string,
    quantity: number,
    created_at: Date,
    updated_at: Date,
    amenity: Amenity
}

export type ServerApartmentImageData = {
    id: string,
    image: string,
    created_at: Date,
    updated_at: Date,
    apartment: string
}

export type ServerApartmentData = {
    id: string,
    user: User,
    country: {
        id: string,
        name: string
    },
    state: {
        id: string,
        name: string,
        country: string
    },
    city: {
        id: string,
        name: string,
        state: string
    },
    school: {
        id: string,
        name: string,
        country: string,
        state: string,
        city: string
    },
    amenities: ServerApartmentAmenityData[],
    nearest_bus_stop: string,
    listing_type: string,
    title: string,
    description: string,
    price: number,
    price_duration: string,
    available_for: string
    is_taken?: boolean,
    is_taken_time?: Date,
    is_taken_number?: number,
    approval_status?: string,
    images: ServerApartmentImageData[],
    video_link: string,
    advert_days_left?: number,
    advert_exp_time?: Date,
    num_of_exp_time_extension?: number
}

export type ApartmentData = {
    total_number_of_apartments: number,
    total_pages: number,
    previous_page: number | null,
    current_page: number,
    next_page: number | null,
    apartments: ServerApartmentData[]
}

// End of Apartment and User data from server.

// Start of Countries, states, cities and schools data from server.

export type School = {
    id: string,
    name: string,
    country: string,
    state: string,
    city: string
}

export type City = {
    id: string,
    state: string,
    name: string,
    schools: School[]
}

export type State = {
    id: string,
    name: string,
    country: string,
    cities: City[]
}

// End of Countries, states, cities and schools data

// Start of components type

export type ImageCarouselProp = {
    images: ServerApartmentImageData[]
}

export type PropertyAmenitiesProp = {
    amenities: ServerApartmentAmenityData[]
}

export type SearchBarProps = {
    setPage?: Dispatch<SetStateAction<number>>
}

export type PaginatedPropertyProps = {
    data: ApartmentData | undefined,
    isSuccess?: boolean,
    isError?: boolean,
    error?: Error | null,
    isLoading?: boolean,
    isPlaceholderData: boolean,
    page: number,
    setPage: Dispatch<SetStateAction<number>>,
    limit: number,
    singularHeader: string,
    pluralHeader: string,
}

export type GetNextOrPrevPageProps = {
    data: ApartmentData;
    isPlaceholderData: boolean;
    page: number;
    limit: number;
    setPage: Dispatch<SetStateAction<number>>;
}

export type NonPaginatedPropertyProps = {
    data: ApartmentData | undefined,
    isSuccess?: boolean,
    isError?: boolean,
    error?: Error | null,
    isLoading?: boolean,
    singularHeader: string,
    pluralHeader: string,
}

export type MenuItems = {
    title: string,
    route?: string,
    children?: MenuItems[]
}

export type DropdownProps = {
    item: MenuItems
    isOpen?: boolean
}

type SpinnerStyle<T> = {
    [key: string]: T;
}

export type SpinnerProps = {
    style?: SpinnerStyle<string>;
}

// End of components type

// Start of hooks type

export type UsePaginatedPropertyProp = {
    page: number,
    queryKey1: string,
    queryKey2?: string,
    url: string
}

// End of hooks type

// Start of the page type
export type SearchPageProps = {
    singularHeading: string;
    pluralHeading: string
}
