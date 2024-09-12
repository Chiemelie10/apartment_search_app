import { getYouTubeVideoId } from "@/utils";
import { useState } from "react";
import Spinner from "./Spinner";

const Video = ({ src, title }: VideoProps) => {
    const [ loading, setLoading ] = useState(true);

    const youTubeVideoId = getYouTubeVideoId(src);
    if (!youTubeVideoId) console.log("Provide YouTube video Id.");

    const handleFrameLoad = () => {
        // Hide the spinner when iframe is loaded.
        setLoading(false);
    }

    return (
        <>
            <div className="overflow-hidden pb-[56.25%] relative">
                { loading && (
                    <Spinner
                        style={{
                            position: "absolute",
                            top: "50%",
                            left: "50%",
                        }}
                    />
                )}
                <iframe
                    src={`https://www.youtube.com/embed/${youTubeVideoId}`}
                    allowFullScreen
                    loading="lazy"
                    // sandbox=""
                    title={title}
                    onLoad={handleFrameLoad}
                    className="border-0 left-0 top-0 w-full h-full absolute"
                />
            </div>
        </>
    )
}

export default Video;
