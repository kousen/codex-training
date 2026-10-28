package com.example.taskapi.dto;

import java.util.List;
import org.springframework.data.domain.Page;

public record TaskPage(List<TaskResponse> content, int page, int size, long totalElements, int totalPages) {
    public static TaskPage from(Page<TaskResponse> tasks) {
        return new TaskPage(tasks.getContent(), tasks.getNumber(), tasks.getSize(),
                tasks.getTotalElements(), tasks.getTotalPages());
    }
}
