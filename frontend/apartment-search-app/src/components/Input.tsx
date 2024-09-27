import usePasswordVisibility from "@/hooks/usePasswordVisibilty";
import { ForwardedRef, ReactNode, Ref, RefAttributes, forwardRef } from "react";
import { FieldValues, UseFormRegister } from "react-hook-form";


function fixedForwardRef<T, P = {}>(
    render: (props: P, ref: Ref<T>) => ReactNode
): (props: P & RefAttributes<T>) => ReactNode {
    return forwardRef(render) as any;
}

const GenericInput = <T extends FieldValues>(
    props: InputProps<T> & ReturnType<UseFormRegister<T>>,
    ref: ForwardedRef<HTMLInputElement>) => {
    const {
        type,
        id,
        value,
        dataTestId,
        onChange,
        onBlur,
        errors,
        dirtyFields,
        handleChange,
        style,
        outerStyle,
        label,
        name,
        ...rest
    } = props;

    // const { inputRef, toggleVisibility, isVisible } = usePasswordVisibility();
    // const { ref, onChange, ...rest } = register(name);

    return (
        <div
            style={outerStyle}
        >
            <input
                {...rest}
                id={id}
                name={name}
                data-testid={dataTestId}
                placeholder={label}
                type={type}
                value={value}
                ref={ref}
                onChange={onChange}
                onBlur={onBlur}
                className="hover: cursor-pointer px-3 rounded-md
                    border border-gray-400 border-solid"
                style={style}
            />
            {
                errors && (
                    <p
                        className="mt-3 text-red-500"
                    >
                        {errors.message}
                    </p>
                )
            }
        </div>
    )
}

const Input = fixedForwardRef(GenericInput);
export default Input;
