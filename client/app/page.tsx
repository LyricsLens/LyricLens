"use client";
import { useState, useEffect } from "react";
import { Search } from "lucide-react";
import Logo from "@/public/logos/LyricLensLogo.png";

function LandingPage() {
	let tempID = 1;
	const [url, setUrl] = useState("");
	type Song = { id: string; title: string; artist: string };
	const [songs, setSongs] = useState<Song[]>([]);
	const [loading, setLoading] = useState(false);
	const [hovering, setHovering] = useState(false);
	const [x, setX] = useState(50);
	const [y, setY] = useState(50);
	const [error, setError] = useState<string | null>(null);
	const API_URL = process.env.REACT_APP_API_URL;
	console.log("api url " + API_URL);
	
	useEffect(() => {
		const interval = setInterval(() => {
			const time = Date.now() / 1500;
			setX(50 + Math.sin(time) * 20);
			setY(50 + Math.cos(time * 0.8) * 20);
		}, 50);
		return () => clearInterval(interval);
	}, []);

	function validateSpotifyUrl(value: string) {
		const r =
			/^(https?:\/\/)?(open\.spotify\.com\/(playlist)\/[A-Za-z0-9]+|spotify:(playlist|album|track):[A-Za-z0-9]+)(\?.*)?$/;
		return r.test(value.trim());
	}

	async function handleAnalyze() {
		setError(null);

		if (!validateSpotifyUrl(url)) {
			setError("Please enter a valid Spotify playlist. We support playlist URLs only.");
			return;
		}

		setLoading(true);
		// --- bing bong the logic goes here ---
		

		postImage();
		setTimeout(() => {
			setLoading(false);
		}, 600);
	}

	async function postImage() {
		console.log("Posting image..")
		try {
			const res = await fetch(`/api/images`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ id: tempID, url: "sample URL" }),
			})
			const data = await res.json();
			console.log(data);
		} catch (err) {
			console.error(err);
		} finally {
			setLoading(false);
			tempID += 1;
		}
	}

	function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
		if (e.key === "Enter" && url && !loading) {
			handleAnalyze();
		}
	}

	return (
		<div className="bg-[#121212] min-h-screen text-gray-200 relative overflow-hidden">
			{/* soft gradient blobs */}
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
			{/* subtle noise */}
			<div
				aria-hidden
				className="pointer-events-none absolute inset-0 opacity-[0.06] mix-blend-overlay"
				style={{
					backgroundImage:
						"url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140' viewBox='0 0 140 140'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/><feComponentTransfer><feFuncA type='table' tableValues='0 0.5'/></feComponentTransfer></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")",
				}}
			/>

			<div className="relative">
				{/* Header / Logo */}
				<header className="px-4 pt-14">
					<div className="mx-auto max-w-3xl text-center">
						<img
							src={Logo.src}
							alt="LyricLens Logo"
							width={1920}
							height={1080}
							className="mx-auto h-14 w-auto opacity-95"
						/>
						<h1 className="mt-6 text-3xl md:text-4xl font-semibold tracking-tight text-white">
							Turn any Spotify playlist into awesomeness
						</h1>
						<p className="mt-3 text-sm md:text-base text-gray-400">
							Paste a link. We&apos;ll surface vibes, themes, and standout tracks.
						</p>
					</div>
				</header>

				{/* Input Card */}
				<main className="px-4 h-full">
					<div className="mx-auto mt-8 max-w-3xl rounded-2xl border border-white/10 bg-white/[.03] backdrop-blur-sm shadow-[0_8px_40px_rgba(0,0,0,.35)]">
						<div className="p-4 md:p-5">
							<label
								htmlFor="spotifyUrl"
								className="sr-only"
							>
								Spotify URL
							</label>

							<div className="flex flex-col md:flex-row gap-3">
								<input
									id="spotifyUrl"
									type="text"
									value={url}
									onChange={(e) => setUrl(e.target.value)}
									onKeyDown={handleKeyDown}
									placeholder="Enter Spotify playlist URL…"
									className="grow px-4 py-3 bg-transparent border border-gray-100/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#1DB954] placeholder-gray-500/80"
									aria-invalid={!!error}
									aria-describedby={error ? "url-error" : undefined}
								/>
								<button
									onClick={handleAnalyze}
									disabled={!url || loading}
									onMouseEnter={() => setHovering(true)}
									onMouseLeave={() => setHovering(false)}
									style={{
										padding: "12px 22px",
										background:
											hovering && !loading && url
												? `radial-gradient(circle at ${x}% ${y}%, #d9f99d 0%, #a3e635 35%, #84cc16 60%, #65a30d 100%)`
												: "white",
										color:
											hovering && !loading && url ? "white" : "#111827",
										border: "1px solid #d1d5db",
										borderRadius: "12px",
										cursor: !url || loading ? "not-allowed" : "pointer",
										transition: "all 0.6s ease",
										display: "flex",
										alignItems: "center",
										gap: "8px",
										opacity: !url || loading ? 0.5 : 1,
										boxShadow:
											hovering && !loading && url
												? "0 12px 30px rgba(132, 204, 22, 0.35)"
												: "0 4px 14px rgba(0,0,0,.15)",
									}}
									aria-live="polite"
								>
									<Search size={18} />
									{loading ? "Analyzing…" : "Analyze"}
								</button>
							</div>

							{/* helper / error */}
							<div className="mt-3 min-h-[1.25rem] text-sm">
								{error ? (
									<p id="url-error" className="text-red-400">
										{error}
									</p>
								) : (
									<p className="text-gray-500">
										Tip: Works with{" "}
										<span className="text-gray-300">
											playlist
										</span>{" "}
										links.
									</p>
								)}
							</div>
						</div>
					</div>

					{/* Results */}
					<div className="mx-auto mt-10 max-w-3xl">
						{songs.length > 0 && (
							<div className="rounded-lg overflow-hidden border border-white/10 bg-white/[.04] backdrop-blur-sm">
								<table className="w-full border-collapse">
									<thead className="bg-white/[.06] border-b border-white/10">
										<tr>
											<th className="px-6 py-3 text-left text-[11px] font-medium tracking-wide text-gray-400">
												#
											</th>
											<th className="px-6 py-3 text-left text-[11px] font-medium tracking-wide text-gray-400">
												SONG
											</th>
											<th className="px-6 py-3 text-left text-[11px] font-medium tracking-wide text-gray-400">
												ARTIST
											</th>
										</tr>
									</thead>
									<tbody>
										{songs.map((song, i) => (
											<tr
												key={song.id}
												className="border-b border-white/5 hover:bg-white/[.03] transition"
											>
												<td className="px-6 py-4 text-sm text-gray-400">
													{i + 1}
												</td>
												<td className="px-6 py-4 text-sm text-gray-100">
													{song.title}
												</td>
												<td className="px-6 py-4 text-sm text-gray-300">
													{song.artist}
												</td>
											</tr>
										))}
									</tbody>
								</table>
							</div>
						)}

						{songs.length === 0 && !loading && (
							<div className="mt-16 text-center">
								<p className="mt-4 text-gray-400">
									Paste a Spotify link to get started.
								</p>
							</div>
						)}
					</div>
				</main>
			</div>
		</div>
	);
}

function Feature({
	icon,
	title,
	text,
}: {
	icon: React.ReactNode;
	title: string;
	text: string;
}) {
	return (
		<div className="flex items-start gap-3 rounded-lg border border-white/10 bg-white/[.02] px-3 py-2">
			<div className="mt-[2px] grid h-6 w-6 place-items-center rounded-md border border-white/10">
				{icon}
			</div>
			<div>
				<p className="text-xs font-semibold text-white">{title}</p>
				<p className="text-xs text-gray-400">{text}</p>
			</div>
		</div>
	);
}

export default LandingPage;