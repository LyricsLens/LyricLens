import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function POST(request: NextRequest) {
  const params = await request.json();
  const { playlist_id } = params;
  const res = await fetch(`${API_URL}/songs?playlist_id=${playlist_id}`);

  if (!res.ok) {
    return NextResponse.json(
      { error: "Failed to fetch songs from external API" },
      { status: res.status }
    );
  }

  const data = await res.json();
  return NextResponse.json(data);
}
