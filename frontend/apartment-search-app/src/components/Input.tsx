const Input = (props: InputProps) => {
    const {type, name, register, id} = props;

    // const { ref, onChange, ...rest } = register(name);

    return (
        <>
            <input
                id={id}
                type={type}
                {...register(name)}
            />
        </>
    )
}

export default Input;