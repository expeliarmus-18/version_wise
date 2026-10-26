package com.versionwise.backend;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(properties = {
		"app.security.jwt-secret=versionwise-test-only-secret-not-for-production-123456789",
		""
})class BackendApplicationTests {

	@Test
	void contextLoads() {
	}

}
