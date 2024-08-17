// const PaginatedPropertySkeleton = () => {
//     return (
//         <div className="w-full">
//             <h1 className="px-4 lg:px-10 font-bold text-xl text-gray-950">
//                 {data.apartments.length === 1
//                     ? singularHeader : pluralHeader
//                 }
//             </h1>
//             <div className="w-full lg:px-6 mt-2">
//                 <ul className="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3
//                         xl:grid-cols-4 gap-6"
//                 >
//                     {data?.apartments?.map((apartment) => (
//                         <Link
//                             href={`/apartment/${apartment.id}`}
//                             key={apartment.id}
//                             className="m-4"
//                         >
//                             <li
//                                 className="
//                                     px-4 py-6 bg-white rounded-xl shadow-md
//                                     hover:shadow-slate-500 hover:shadow-lg
//                                 "
//                             >
//                                 <ImageCarousel images={apartment.images} />
//                                 <h2 className="font-bold mt-2">
                                    
//                                     {capitalize(apartment.title)}
//                                 </h2>
//                                 {apartment.description && (
//                                     <p
//                                         className="line-clamp-2 mt-2">
//                                             {capitalize(apartment.description)}
//                                     </p>
//                                 )}
//                                 <p className="mt-2">
//                                     <span className="font-bold">Location: </span>
//                                     <span>{capitalize(apartment.city.name)}, </span>
//                                     <span>{capitalize(apartment.state.name)}</span>
//                                 </p>
//                                 <p className="mt-2">
//                                     <span className="font-bold">Type: </span>
//                                     <span>{capitalize(apartment.listing_type)}</span>
//                                 </p>
//                                 <p className="mt-2">
//                                     <span className="font-bold">Cost: </span>
//                                     <span>NGN {apartment.price} / year</span>
//                                 </p>
//                             </li>
//                         </Link>
//                     ))}
//                 </ul>
//             </div>
//             <GetNextOrPrevPage
//                 data={data}
//                 isPlaceholderData={isPlaceholderData}
//                 page={page}
//                 limit={limit}
//                 setPage={setPage}
//             />
//         </div>
//     )
// }