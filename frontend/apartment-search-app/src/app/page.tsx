import { SearchBarContextProvider } from "@/context/SearchBarContext";
import Home from "@/pages/Home";

const HomePage = () => {
  return (
    <SearchBarContextProvider>
      <Home />
    </SearchBarContextProvider>
  )
}

export default HomePage;
