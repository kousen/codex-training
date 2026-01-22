package com.example.taskapi.service;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.UpdateTaskRequest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface TaskService {

    TaskResponse create(CreateTaskRequest request);

    TaskResponse getById(Long id);

    Page<TaskResponse> list(Pageable pageable);

    TaskResponse update(Long id, UpdateTaskRequest request);

    void delete(Long id);
}
