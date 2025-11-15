"use client";
import { useRouter } from "next/navigation";
export default function PortfolioPage() {
    const router = useRouter();
    //Sample images for now
    let images: string[] = [
        "https://picsum.photos/id/237/200/300",
        "https://picsum.photos/seed/picsum/200/300",
        "https://picsum.photos/200/300?grayscale",
        "https://picsum.photos/200/300"
    ];
    
    return (
        <div className="p-6">
            <button onClick={() => router.push("/")} className="text-[14px] bg-white/10 hover:bg-white/20 transition-colors duration-200 text-white font-medium py-2 px-4 rounded-lg">
                ← Back to Home
            </button>
            <h1 className="text-3xl font-bold" style={{ textAlign: "center", paddingBottom: "1em" }}>Portfolio Page</h1>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {images.map((url, index) => (
                    <img
                        key={index}
                        src={url}
                        alt={`Portfolio image ${index + 1}`}
                        className="w-96 h-96 object-cover rounded-md shadow-md"
                    />
                ))}
            </div>
        </div>
    );
}
