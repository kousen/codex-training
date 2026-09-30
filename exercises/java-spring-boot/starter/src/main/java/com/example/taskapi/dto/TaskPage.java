package com.example.taskapi.dto;

import java.util.List;
import org.springframework.data.domain.Page;

public record TaskPage(List<TaskResponse> content, int page, int size, long totalElements, int totalPages) {
    public static TaskPage from(Page<TaskResponse> result) {
        return new TaskPage(result.getContent(), result.getNumber(), result.getSize(),
            result.getTotalElements(), result.getTotalPages());
    }
}
