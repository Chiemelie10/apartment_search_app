import { DetailedApartmentContextProvider } from "@/context/DetailedApartmentContext";
import Apartment from "@/pages/Apartment";

const SingleApartmentPage = () => {
  return (
    <DetailedApartmentContextProvider>
      <Apartment />
    </DetailedApartmentContextProvider>
  )
}
  
export default SingleApartmentPage;
