/** @type {import('next').NextConfig} */
const nextConfig = {
    /**
     * @improvement: calculate urls on the server and don't expose them to the client
     */
    env: {
        APP_API_URL: process.env.APP_API_URL,
    },
};

export default nextConfig;