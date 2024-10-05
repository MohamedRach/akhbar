import { useEffect, useState } from "react";
import { useNews } from "./api/newsList";
import "./App.css";
import NewsCard from "./components/NewsCard";
import { Button } from "./components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import { filterNewsBySource } from "./lib/utils";
import { News } from "./types/News";

function App() {
  const { data, error, isLoading } = useNews();
  const [news, setNews] = useState<News[] | undefined>(data);

  const handleNewsSource = (source: string) => {
    setNews(filterNewsBySource(data, source));
  };

  useEffect(() => {
    if (data) {
      setNews(data);
    }
  }, [data]);
  return (
    <>
      <div className=" flex flex-row gap-[650px] h-14 bg-black">
        <h3 className="mt-3 ml-3 text-white font-bold text-2xl">Akhbar</h3>
      </div>
      <Select onValueChange={handleNewsSource}>
        <SelectTrigger className="mt-4 ml-4 w-[280px] h-[75px]">
          <SelectValue placeholder="Source" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="assabah">Assabah</SelectItem>
          <SelectItem value="hespress">Hespress</SelectItem>
          <SelectItem value="hibapress">Hibapress</SelectItem>
          <SelectItem value="alalam">Alalam</SelectItem>
        </SelectContent>
      </Select>
      <div className="grid grid-cols-3 mt-4 ml-2 mr-2 gap-12">
        {news?.map((element) => <NewsCard news={element}></NewsCard>)}
      </div>
    </>
  );
}

export default App;
