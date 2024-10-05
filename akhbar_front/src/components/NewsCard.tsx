import { News } from "@/types/News";
import { Badge } from "./ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";

function NewsCard({ news }: { news: News }) {
  const { id, title, link, source, image, created_at } = news;

  return (
    <a href={link} target="_blank">
      <Card key={id}>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>
            <Badge>{source}</Badge>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <img className="w-full" src={image} alt={title} />
        </CardContent>
        <CardFooter>
          <p>{new Date(created_at).toLocaleDateString()}</p>
        </CardFooter>
      </Card>
    </a>
  );
}

export default NewsCard;
