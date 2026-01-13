// Copyright (c) 2026 Cumulonimbus Crew. All rights reserved.
import { useRouter } from "next/navigation";

export default function Navbar() {
    const router = useRouter();
    const handleClick = () => {
        router.push("/portfolio");
    }
    return (
        <nav className="w-full p-6 flex items-center justify-end">
            <button onClick={handleClick} type="button" className="text-[14px] bg-white/10 hover:bg-white/20 transition-colors duration-200 text-white font-medium py-2 px-4 rounded-lg">
                View our Portfolio
            </button>
        </nav>
    )
}