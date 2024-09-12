const TextArea = <T extends unknown>(props: TextAreaProps<T>) => {
    const {name, register, id, value, dataTestId, style} = props;
    return (
        <div>
            <textarea
                id={id}
                data-testid={dataTestId}
                {...register(name)}
                style={style}
                value={value}
            >
            </textarea>
        </div>
    )
}

export default TextArea;
