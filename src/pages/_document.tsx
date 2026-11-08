import { Head, Html, Main, NextScript } from "next/document";
import { BRAND_NAME } from "@/constants";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "";
const DESCRIPTION =
  "Play live chess and analyze your games for free with Stockfish.";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <meta name="description" content={DESCRIPTION} />

        {/* OG (Social networks) */}
        <meta property="og:title" content={BRAND_NAME} />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content={BRAND_NAME} />
        {SITE_URL && <meta property="og:url" content={`${SITE_URL}/`} />}
        <meta
          property="og:image"
          content={`${SITE_URL}/social-networks-1200x630.png`}
        />
        <meta property="og:description" content={DESCRIPTION} />

        {/* Twitter */}
        <meta name="twitter:title" content={BRAND_NAME} />
        <meta name="twitter:description" content={DESCRIPTION} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta
          name="twitter:image"
          content={`${SITE_URL}/social-networks-1200x630.png`}
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
