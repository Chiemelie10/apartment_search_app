import { isAxiosError } from "axios";
import { useForm, SubmitHandler, FieldValues, Path } from "react-hook-form";
import { UseSubmitFormProps, UseSubmitFormReturn, ErrorResponse } from "@/interfaces";
import { useRouter } from "next/router";


const useSubmitForm = <TFormData extends FieldValues, TResponse>({
    mutateAsync, defaultValues, pathname = null, query = null
}: UseSubmitFormProps<TFormData, TResponse>): UseSubmitFormReturn<TFormData> => {
    const router = useRouter();

    const isFormErrorKey = <TFormData extends FieldValues>(
        key: string, defaultValues?: TFormData): key is Path<TFormData> => {
            if (!defaultValues) {
                return false;
            }
            return key in defaultValues;
        }

    const {
        register,
        handleSubmit,
        clearErrors,
        setError,
        control,
        formState: { errors, isSubmitting, dirtyFields },
    } = useForm<TFormData>(defaultValues);

    const onSubmit: SubmitHandler<TFormData> = async (data) => {
        if (pathname && query) {
            router.push({pathname: pathname, query: query});
        } else {
            try {
                const response = await mutateAsync(data);
                console.log(response);
            } catch (error) {
                if (isAxiosError<TFormData>(error)
                    && error.response && error.response.data) {
                    for (let [field_name, messages] of Object.entries(
                        error.response.data as ErrorResponse
                        )) {
                        if (isFormErrorKey<TFormData>(field_name, defaultValues) ||
                            "root.error" || "root.non_field_errors") {
                            setError(field_name as Path<TFormData>, { type: "api", message: messages[0] });
                        }
                    }
                }
                console.error(error);
            }
        }
    }

    return {onSubmit, register, handleSubmit, control, errors, isSubmitting, dirtyFields};
}

export default useSubmitForm;