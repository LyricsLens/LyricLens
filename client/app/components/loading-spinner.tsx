export default function LoadingLogo() {
    return (
        <div className="flex items-center justify-center w-full h-full">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 37.08 31.87"
                width="90"
                height="90"
            >
                <style>
                    {`
            .bar {
              fill: #ffffff;
              transform-origin: center;
              animation: pulse 1.4s infinite ease-in-out;
            }

            .bar-1 { animation-delay: 0s; }
            .bar-2 { animation-delay: 0.12s; }
            .bar-3 { animation-delay: 0.24s; }
            .bar-4 { animation-delay: 0.36s; }
            .bar-5 { animation-delay: 0.48s; }

            @keyframes pulse {
              0%, 100% {
                transform: scale(1);
                opacity: 0.5;
              }
              50% {
                transform: scale(1.15);
                opacity: 1;
              }
            }
          `}
                </style>

                <g id="Layer_1-2" data-name="Layer 1">
                    <g>
                        {/* center bar */}
                        <path
                            className="bar bar-3"
                            d="M18.54,31.87c-1.38,0-2.5-1.12-2.5-2.5V2.5c0-1.38,1.12-2.5,2.5-2.5s2.5,1.12,2.5,2.5v26.87c0,1.38-1.12,2.5-2.5,2.5Z"
                        />
                        {/* right mid */}
                        <path
                            className="bar bar-4"
                            d="M26.56,29.41c-1.38,0-2.5-1.12-2.5-2.5V4.95c0-1.38,1.12-2.5,2.5-2.5s2.5,1.12,2.5,2.5v21.96c0,1.38-1.12,2.5-2.5,2.5Z"
                        />
                        {/* left mid */}
                        <path
                            className="bar bar-2"
                            d="M10.52,29.41c-1.38,0-2.5-1.12-2.5-2.5V4.96c0-1.38,1.12-2.5,2.5-2.5s2.5,1.12,2.5,2.5v21.96c0,1.38-1.12,2.5-2.5,2.5Z"
                        />
                        {/* far right */}
                        <path
                            className="bar bar-5"
                            d="M34.58,26.99c-1.38,0-2.5-1.12-2.5-2.5V7.38c0-1.38,1.12-2.5,2.5-2.5s2.5,1.12,2.5,2.5v17.11c0,1.38-1.12,2.5-2.5,2.5Z"
                        />
                        {/* far left */}
                        <path
                            className="bar bar-1"
                            d="M2.5,26.99c-1.38,0-2.5-1.12-2.5-2.5V7.38c0-1.38,1.12-2.5,2.5-2.5s2.5,1.12,2.5,2.5v17.11c0,1.38-1.12,2.5-2.5,2.5Z"
                        />
                    </g>
                </g>
            </svg>
        </div>
    );
}