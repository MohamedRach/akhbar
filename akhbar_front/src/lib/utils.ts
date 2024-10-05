import { News } from "@/types/News";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const filterNewsBySource = (
  newsList: News[] | undefined,
  source: string,
): News[] | undefined => {
  return newsList?.filter(
    (news) => news.source.toLowerCase() === source.toLowerCase(),
  );
};
