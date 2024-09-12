const Input = <T extends unknown>(props: InputProps<T>) => {
    const {type, name, register, id, value, dataTestId} = props;

    // const { ref, onChange, ...rest } = register(name);

    return (
        <>
            <input
                id={id}
                data-testid={dataTestId}
                type={type}
                value={value}
                {...register(name)}
                className="hover: cursor-pointer"
            />
        </>
    )
}

export default Input;