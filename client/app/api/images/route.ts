// Copyright (c) 2026 Cumulonimbus Crew. All rights reserved.
import { NextRequest, NextResponse } from "next/server";

const baseApiUrl = process.env.NEXT_PUBLIC_API_URL;

export async function POST(request: NextRequest) {
  const params = await request.json();
  const { id, url } = params;
  console.log(`${baseApiUrl}/images`);
  try {
    const res = await fetch(`${baseApiUrl}/images`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, url: url }),
    });
    console.log("Response from external API:", res);
    return NextResponse.json(await res.json());
  } catch (err) {
    return NextResponse.json(
      {
        error: "Failed to post image",
        message: err instanceof Error ? err.message : String(err),
      },
      { status: 500 }
    );
  }
}
