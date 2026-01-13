// Copyright (c) 2026 Cumulonimbus Crew. All rights reserved.
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const params = await request.json();
  const { playlist_id, API_URL } = params;

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
