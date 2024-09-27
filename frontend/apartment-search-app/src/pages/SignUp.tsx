"use client"

import axiosInstance from "@/api/axios";
import Input from "@/components/Input";
import { useMutation } from "@tanstack/react-query";
import { useId } from "react";
import SignUpSchema, { SignUpFormFields } from "@/schema/signUpSchema";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import useOnSubmit from "@/hooks/useOnSubmit";


const SignUp = () => {
    const {
        register,
        handleSubmit,
        clearErrors,
        setError,
        control,
        formState: { errors, isSubmitting, dirtyFields },
    } = useForm<SignUpFormFields>({
        defaultValues: {
            username: "",
            email: "",
            password: "",
            confirmPassword: ""
        },
        resolver: zodResolver(SignUpSchema)
    });

    const { mutateAsync } = useMutation<User, Error, SignUpFormFields>({
        mutationFn: async(data: SignUpFormFields): Promise<User> => {
            const response = await axiosInstance.post<User>("/auth/register", data);
            return response.data
        }
    })

    const defaultValues = {
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
    }

    const onSubmit = useOnSubmit<SignUpFormFields, User>({mutateAsync, defaultValues, setError})

    const handleChange = () => {
        if (errors.root) {
            clearErrors("root");
        }
    }


    const id = useId();

    return (
        <div
            className="flex justify-center bg-blue-300 px-4 lg:px-10"
        >
            <form onSubmit={handleSubmit(onSubmit)}
                className="my-10 flex flex-col w-full md:w-[65%] lg:w-[55%] max-w-[50rem]
                    bg-gray-100 shadow-lg p-5 rounded-lg"
            >
                <div className="flex flex-col">
                    <label
                        htmlFor={`username-${id}`}
                        className="mb-3 hover:cursor-pointer font-bold hidden md:inline-block w-fit"
                    >
                        Username:
                    </label>
                    <Input<SignUpFormFields>
                        {...register("username")}
                        id={`username-${id}`}
                        label="Username"
                        // name="username"
                        dataTestId="SignUp-username"
                        type="text"
                        errors={errors.username}
                        handleChange={handleChange}
                        style={{
                            height: "2.5rem",
                            width: "100%"
                        }}
                        outerStyle={{
                            marginBottom: "1.4rem"
                        }}
                    />
                </div>
                <div className="flex flex-col">
                    <label
                        htmlFor={`email-${id}`}
                        className="mb-3 hover:cursor-pointer font-bold hidden md:inline-block w-fit"
                    >
                        Email:
                    </label>
                    <Input<SignUpFormFields>
                        {...register("email")}
                        id={`email-${id}`}
                        label="Email"
                        // name="email"
                        dataTestId="SignUp-email"
                        type="email"
                        errors={errors.email}
                        handleChange={handleChange}
                        style={{
                            height: "2.5rem",
                            width: "100%"
                        }}
                        outerStyle={{
                            marginBottom: "1.4rem"
                        }}
                    />
                </div>
                <div className="flex flex-col">
                    <label
                        htmlFor={`password-${id}`}
                        className="mb-3 hover:cursor-pointer font-bold hidden md:inline-block w-fit"
                    >
                        Password:
                    </label>
                    <Input<SignUpFormFields>
                        {...register("password")}
                        id={`password-${id}`}
                        label="Password"
                        // name="password"
                        dataTestId="SignUp-password"
                        type="password"
                        dirtyFields={dirtyFields}
                        errors={errors.password}
                        handleChange={handleChange}
                        style={{
                            height: "2.5rem",
                            width: "100%"
                        }}
                        outerStyle={{
                            marginBottom: "1.4rem"
                        }}
                    />
                </div>
                <div className="flex flex-col">
                    <label
                        htmlFor={`confirmPassword-${id}`}
                        className="mb-3 hover:cursor-pointer font-bold hidden md:inline-block w-fit"
                    >
                        Confirm password:
                    </label>
                    <Input<SignUpFormFields>
                        {...register("confirmPassword")}
                        id={`confirm-password-${id}`}
                        label="Confirm password"
                        // name="confirmPassword"
                        dataTestId="SignUp-confirmPassword"
                        type="password"
                        dirtyFields={dirtyFields}
                        errors={errors.confirmPassword}
                        handleChange={handleChange}
                        style={{
                            height: "2.5rem",
                            width: "100%"
                        }}
                        outerStyle={{
                            marginBottom: "2.4rem"
                        }}
                    />
                </div>
                <button
                    type="submit"
                    className="h-10 w-[100%] sm:w-[30%] md:w-[35%] lg:max-w-[20rem] rounded-lg
                        bg-cyan-400 font-semibold hover:bg-cyan-500
                        flex items-center justify-center self-center
                    "
                >
                    Sign up
                </button>
            </form>
        </div>
    )
}

export default SignUp;
