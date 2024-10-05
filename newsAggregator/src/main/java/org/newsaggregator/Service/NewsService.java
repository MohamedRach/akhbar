package org.newsaggregator.Service;

import org.newsaggregator.Model.News;
import org.newsaggregator.Repository.NewsRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NewsService {

    private NewsRepository newsRepository;

    public NewsService(NewsRepository newsRepository) {
        this.newsRepository = newsRepository;
    }

    public List<News> getNews() {
        return this.newsRepository.findAll();
    }

    public News getNewsById(Integer id) {
        return this.newsRepository.getReferenceById(id);
    }
}
