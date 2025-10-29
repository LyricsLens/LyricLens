
import Logo from "@/public/logo/FullLogo.png"
import Link from "next/link"

export default function Navbar() {
    return (
        <nav className="w-full p-4 border-b border-white/20 mb-8">
            <div className="max-w-7xl mx-auto px-4">
                <Link href="/">
                    <div id="logo-container" className="w-32">
                        <img src={Logo.src} alt="LyricLens Logo" width={1920} height={1080} />
                    </div>
                </Link>
            </div>
        </nav>
    )
}