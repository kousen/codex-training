package com.example.taskapi.unit;

import com.example.taskapi.exception.GlobalExceptionHandler;
import java.sql.SQLException;
import org.junit.jupiter.api.Test;
import org.springframework.dao.DataIntegrityViolationException;
import static org.assertj.core.api.Assertions.*;

class GlobalExceptionHandlerTest {
    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test void unexpectedErrorsDoNotExposeInternals() {
        var result = handler.unexpected(new RuntimeException("secret database details"));
        assertThat(result.getStatus()).isEqualTo(500);
        assertThat(result.getDetail()).doesNotContain("secret");
    }

    @Test void unknownConstraintsRemainInternalErrors() {
        for (String name : new String[] {null, "other_constraint"}) {
            var cause = new org.hibernate.exception.ConstraintViolationException("secret", new SQLException(), name);
            var result = handler.integrity(new DataIntegrityViolationException("secret", cause));
            assertThat(result.getStatus()).isEqualTo(500);
            assertThat(result.getDetail()).doesNotContain("secret");
        }
        assertThat(handler.integrity(new DataIntegrityViolationException("secret")).getStatus()).isEqualTo(500);
    }
}
