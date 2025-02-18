const Button = (props: ButtonProps) => {
    const { type, label, style } = props;

    return (
        <button
            type={type}
            className="text-black bg-cyan-300 text-base font-semibold
                py-1 px-2 rounded-sm hover:opacity-80"
            style={style ? style : undefined}
        >
            {label}
        </button>
    )
}

export default Button;
