import { isFormErrorKey } from "@/utils";
import { isAxiosError } from "axios";
import { FieldValues, Path, SubmitHandler } from "react-hook-form";

const useOnSubmit = <TFormData extends FieldValues, TResponse>(
    {mutateAsync, defaultValues, setError}: useOnSubmitProps<TFormData, TResponse>) => {
    const onSubmit: SubmitHandler<TFormData> = async (data) => {
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
        }
    }

    return onSubmit;
}

export default useOnSubmit;
