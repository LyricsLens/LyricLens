// Copyright (c) 2026 Cumulonimbus Crew. All rights reserved.
"use client";

import { useRouter } from "next/navigation";
import LoadingSpinner from "../components/loading-spinner";
import { useEffect, useState } from "react";

export default function PortfolioPage() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    const router = useRouter();
    const [loading, setLoading] = useState(true);
    const [imageURLs, setImageURLS] = useState<string[]>([]);

    useEffect(() => {
        async function loadData() {
            try {
                const res = await fetch(`${API_URL}/images`);
                const data = await res.json();
                const urls = data.map((obj: { url: string; id: string }) => obj.url);
                setImageURLS(urls);
            } catch (err) {
                console.error("Failed to load images", err);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, []);

    if (loading) {
        return <div className="flex items-center flex-col justify-center min-h-screen bg-[#121212]">
            <LoadingSpinner />
            <h1 className="text-gray-200 mt-4 text-2xl font-bold">Loading our portfolio</h1>
        </div>
    }

    return (
        <div className="bg-[#121212] min-h-screen text-gray-200 relative overflow-hidden">
            <div
                aria-hidden
                className="pointer-events-none absolute inset-0"
                style={{
                    background:
                        "radial-gradient(600px 300px at 70% -10%, rgba(163, 230, 53, 0.15), transparent 60%), radial-gradient(500px 260px at 10% 20%, rgba(217, 249, 157, 0.12), transparent 60%)",
                    maskImage:
                        "radial-gradient(1000px 600px at 50% -10%, black, transparent 80%)",
                }}
            />
            <div
                aria-hidden
                className="pointer-events-none absolute inset-0 opacity-[0.06] mix-blend-overlay"
                style={{
                    backgroundImage:
                        "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140' viewBox='0 0 140 140'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/><feComponentTransfer><feFuncA type='table' tableValues='0 0.5'/></feComponentTransfer></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")",
                }}
            />

            <div className="relative">
                <main className="px-4 pt-10 pb-16">
                    <div className="mx-auto max-w-5xl">
                        <button
                            onClick={() => router.push("/")}
                            className="text-[13px] mb-4 inline-flex items-center gap-1 rounded-lg border border-white/15 bg-white/[.02] px-3 py-1.5 text-gray-200 hover:bg-white/[.06] hover:border-white/30 transition-colors"
                        >
                            <span className="text-base">←</span>
                            <span>Back to Home</span>
                        </button>

                        <div className="mt-4 rounded-2xl border border-white/10 bg-white/[.03] backdrop-blur-sm shadow-[0_8px_40px_rgba(0,0,0,.35)]">
                            <div className="p-5 md:p-7">
                                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-6">
                                    <div>
                                        <h1 className="text-2xl md:text-3xl font-semibold tracking-tight text-white">
                                            Portfolio
                                        </h1>
                                        <p className="mt-1 text-sm text-gray-400">
                                            A sample gallery of generated visuals and artwork.
                                        </p>
                                    </div>
                                </div>

                                {/* Image grid */}
                                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
                                    {imageURLs.map((url, index) => (
                                        <div
                                            key={index}
                                            className="group overflow-hidden rounded-xl border border-white/10 bg-black/30 shadow-[0_6px_26px_rgba(0,0,0,.45)]"
                                        >
                                            <img
                                                src={url}
                                                alt={`Portfolio image ${index + 1}`}
                                                className="w-full aspect-square object-cover transition-transform duration-300 group-hover:scale-105"
                                            />
                                        </div>
                                    ))}
                                </div>

                                {/* Optional footer text */}
                                <p className="mt-5 text-xs text-gray-500 text-center">
                                    These are sample images for layout preview. Your generated
                                    playlist visuals will appear here in the future.
                                </p>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}