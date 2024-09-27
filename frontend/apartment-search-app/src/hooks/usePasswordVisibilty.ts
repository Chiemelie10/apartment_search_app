import { useState, useEffect, useRef } from "react";

const usePasswordVisibility = () => {
    const [shouldFocus, setShouldFocus] = useState(false);
    const [isVisible, setIsVisible] = useState(false)
    const inputRef = useRef<HTMLInputElement | null>(null);

    const toggleVisibility = () => {
        setIsVisible(!isVisible);
        setShouldFocus(true);
    }

    useEffect(() => {
        if (inputRef.current && shouldFocus) {
            inputRef.current.setSelectionRange(-1, -1);
            inputRef.current.focus();
            setShouldFocus(false);
        }
    }, [shouldFocus]);

    return {
        isVisible,
        inputRef,
        toggleVisibility
    }
}

export default usePasswordVisibility;