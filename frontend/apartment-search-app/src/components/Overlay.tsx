const Overlay = ({removeOverlay}: OverlayProps) => {
    return (
        <div
            onClick={removeOverlay}
            className={
                `w-full min-h-screen fixed inset-0 bg-black
                bg-opacity-50 z-20`
            }
        ></div>
    )
}

export default Overlay;
