import { z } from "zod";


const SignUpSchema = z.object({
    username: z
        .string()
        .min(1, { message: "Username is required" }
    ),
    email: z
        .string()
        .min(1, { message: "Email is required" })
        .email(),
    password: z
        .string()
        .min(1, { message: "Password is required" })
        .min(8, {message: "Password cannot be less than 8 characters."})
        .regex(/^(?=.*[a-zA-Z])(?=.*[0-9])/, {message: "Password is not alphanumeric."}
    ),
    confirmPassword: z
        .string()
}).refine(data => data.password === data.confirmPassword, {
    message: "Passwords do not match.",
    path: ['confirmPassword']
});

export type SignUpFormFields = z.infer<typeof SignUpSchema>;
export default SignUpSchema;
