package org.newsaggregator.Controller;

import org.newsaggregator.Model.News;
import org.newsaggregator.Service.NewsService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class NewsController {

    private NewsService newsService;

    public NewsController(NewsService newsService) {
        this.newsService = newsService;
    }

    @CrossOrigin
    @GetMapping(path="/news")
    public List<News> getNews() {
        return newsService.getNews();
    }

    @RequestMapping("/news/{id}")
    public News getNewsById(@PathVariable String id) {
        Integer newsId = Integer.parseInt(id);
        return newsService.getNewsById(newsId);
    }

}
