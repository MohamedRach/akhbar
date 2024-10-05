import { News } from "@/types/News";
import axios from "axios";
import { useQuery } from "react-query";

// Function to fetch the list of news
const fetchNews = async (): Promise<News[]> => {
  const response = await axios.get<News[]>("http://localhost:8080/news");
  return response.data;
};

// Custom hook to get the list of news
export const useNews = () => {
  return useQuery<News[], Error>(["news"], fetchNews);
};
