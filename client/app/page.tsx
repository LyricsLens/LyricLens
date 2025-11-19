"use client";
import { useState, useEffect } from "react";
import { Search } from "lucide-react";
import Logo from "@/public/logos/LyricLensLogo.png";
import Navbar from "./components/navbar";

function LandingPage() {
	const [url, setUrl] = useState("");
	type Song = { title: string; artist: string; lyrics: string };
	const [songs, setSongs] = useState<Song[]>([]);
	const [loading, setLoading] = useState(false);
	const [hovering, setHovering] = useState(false);
	const [x, setX] = useState(50);
	const [y, setY] = useState(50);
	const [error, setError] = useState<string | null>(null);
	const [imageUrl, setImageUrl] = useState<string | null>(null);
	const API_URL = process.env.NEXT_PUBLIC_API_URL;
	type Themes =
		| string
		| string[]
		| {
			summary?: string;
			description?: string;
			overall_theme?: string;
			keywords?: string[];
			moods?: string[];
			[key: string]: unknown;
		};
	const [themes, setThemes] = useState<Themes | null>(null);

	type ImageType = {
		id: string;
		url: string;
		prompt?: string;
		createdAt?: string;
	};
	const [images, setImages] = useState<ImageType[]>([]);

	useEffect(() => {
		async function fetchImages() {
			try {
				const res = await fetch(`${API_URL}/images`);
				if (!res.ok) return;
				const data = await res.json(); 
				console.log("Data pulled from dynamo fetch: ", data)
				setImages(data);
			} catch (err) {
				console.error("Error fetching images", err);
			}
		}
		fetchImages();
	}, [API_URL]);


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


	async function buildPromptFromThemes(playlistId: string): Promise<string> {
		try {
			const res = await fetch(`${API_URL}/themes?playlist_id=${playlistId}`);
			if (!res.ok) {
				console.error("failed to fetch themes:", res.status);
				return "abstract, moody album cover art inspired by this playlist";
				// generic prompt ^
			}

			const data = await res.json();
			console.log("Themes response:", data);
			setThemes(data);

			let summary = "";
			let keywords: string[] = [];

			if (typeof data === "string") {
				summary = data;
			} else if (Array.isArray(data)) {
				keywords = data.slice(0, 8).map(String);
			} else if (typeof data === "object" && data !== null) {
				summary =
					(data.summary as string) ||
					(data.description as string) ||
					(data.overall_theme as string) ||
					"";

				if (Array.isArray(data.keywords)) {
					keywords = data.keywords.slice(0, 8).map(String);
				} else if (Array.isArray(data.moods)) {
					keywords = data.moods.slice(0, 8).map(String);
				}
			}

			const keywordsText = keywords.length ? keywords.join(", ") : "";
			const themeText = [summary, keywordsText].filter(Boolean).join(". ");

			const prompt = `
				highly detailed album cover illustration capturing the overall mood of this playlist;
				${themeText || "emotional, atmospheric, playlist-inspired artwork"};
				cinematic lighting, rich colors, expressive character and environment, 16:9 aspect ratio
			`.replace(/\s+/g, " ").trim();

			return prompt;
		} catch (err) {
			console.error("error fetching themes:", err);
			return "abstract, moody album cover art inspired by this playlist";
			// again, a generic prompt ^
		}
	}

	async function handleAnalyze() {
		setSongs([]);
		setError(null);
		const sanitized_url = url.split("?")[0]
		if (!validateSpotifyUrl(sanitized_url)) {
			setError("Please enter a valid Spotify playlist. We support playlist URLs only.");
			return;
		}
		const match = sanitized_url.match(/playlist\/([a-zA-Z0-9]+)/);
		if(!match) {
			return;
		}
		console.log('match', match) 
		const playlist_id = match[1]
		setLoading(true);
		// --- bing bong the logic goes here ---

		const res = await fetch(`${API_URL}/songs?playlist_id=${playlist_id}`);
		if (!res.ok) {
			setError("Failed to fetch songs. Please check the playlist URL and try again.");
			setLoading(false);
			return;
		}
		
		const data = await res.json();
		console.log('data', data);
		setSongs(data);

		const prompt = await buildPromptFromThemes(playlist_id);
		console.log("Generated prompt from themes:", prompt);

		await generateImage(prompt);

		//TODO this will need to be longer and we will probably need a better signal since playlist time is not constant
		setTimeout(() => {
			setLoading(false);
		}, 600);
	}

	async function generateImage(prompt: string) {
		console.log(" Generatingimage..");
		
		try {
			const res = await fetch(`${API_URL}/generate_images`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					prompt,
					width: 512,
					height: 512,
					cfgScale: 8,
				}),
			});

			const data = await res.json();
			console.log("image generation data:", data);

			if (!res.ok) {
				console.error(
					"image generation failed:",
					data.error ?? data.message ?? "Unknown error from image generator."
				);
				return;
			}

			if (data.url && data.id) {
				setImageUrl(data.url);

				const image: ImageType = {
					id: data.id,
					url: data.url,
					prompt,
					createdAt: data.createdAt ?? new Date().toISOString(),
				};

				await postImage(image);
				setImages((prev) => [image, ...prev]); // update gallery before
			} else if (data.imageBase64) {
				console.log(" Using base64..");
				const dataUrl = `data:image/png;base64,${data.imageBase64}`;
				setImageUrl(dataUrl);
			}
		} catch (err) {
			console.error("image generation error:" + err);
		} 
	}

	async function postImage(image: ImageType) {
		console.log("Posting image..");
		try {
			const res = await fetch(`${API_URL}/images`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(image),
			});
			const data = await res.json();
			console.log("POST /images response:", data);
		} catch (err) {
			console.error("Error posting image:", err);
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
				<Navbar />
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
							{error && (
								<div className="mt-3 min-h-[1.25rem] text-sm">
									<p id="url-error" className="text-red-400">
										{error}
									</p>
								</div>
							)}
						</div>
					</div>

					{/* Results */}
					<div className="mx-auto mt-10 max-w-3xl">
						Generated image:
						{imageUrl && (
						<div className="mt-6">
							<img
							src={imageUrl}
							alt="Generated image"
							className="w-full max-w-md rounded-lg border border-white/10 shadow-lg"
							/>
						</div>
						)}

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
												key={i}
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

				<section id="services-used" className="mt-20 py-16 px-4 from-[#171717] to-[#121212] bg-linear-to-b">
					<h2 className="text-lg font-semibold text-white mb-6 text-center">
						Features
					</h2>
					<div className="mx-auto max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-4">
						<Feature
							title="Deep Analysis"
							text="We dive into lyrics, moods, and themes to give you a comprehensive overview of your playlist."
						/>
						<Feature
							title="Standout Tracks"
							text="Identify key songs that define the vibe of your playlist."
						/>
						<Feature
							title="Easy to Use"
							text="Just paste your Spotify playlist link and let us do the rest."
						/>
					</div>
				</section>
			</div>
		</div>
	);
}

function Feature({
	icon,
	title,
	text,
}: {
	icon?: React.ReactNode;
	title: string;
	text: string;
}) {
	return (
		<div className="flex items-start gap-3 rounded-lg border border-white/10 bg-white/2 px-5 py-5">
			{icon && (
				<div className="mt-0.5 grid h-6 w-6 place-items-center rounded-md border border-white/10">
					{icon}
				</div>
			)}
			<div>
				<p className="text-sm font-semibold text-white">{title}</p>
				<p className="text-sm text-gray-400">{text}</p>
			</div>
		</div>
	);
}

export default LandingPage;