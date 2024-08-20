import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import CustomQueryClientProvider from "@/context/QueryClientContext";
import Header from "@/components/Header";
import Footer from "@/components/Footer";


const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Property Solutions",
  description: "Explore wide range of properties with our app, where you can easily buy, sell, rent \
                or find shared houses and apartments. Whether you're searching for your dream home or \
                looking to invest in real estate, our platform offers the best options to suit your \
                needs.",
};

export default function RootLayout({children,}: Readonly<{children: React.ReactNode;}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CustomQueryClientProvider>
          <div className="flex flex-col min-h-screen">
            <section><Header /></section>
            <main>{children}</main>
            <section className="mt-auto"><Footer /></section>
          </div>
        </CustomQueryClientProvider>
      </body>
    </html>
  );
}
