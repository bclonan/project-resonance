import http from 'k6/http';
import { check, sleep, group } from 'k6';

// --- Test Configuration ---
// This configuration is designed to put a significant but stable load on the system.
export const options = {
    stages: [
        { duration: '5s', target: 50 },  // Ramp up to 50 virtual users over 5 seconds
        { duration: '10s', target: 50 }, // Stay at 50 virtual users for 10 seconds
        { duration: '5s', target: 0 },   // Ramp down to 0 users
    ],
    thresholds: {
        'http_req_failed': ['rate<0.01'], // Fail the test if more than 1% of requests fail
        'http_req_duration': ['p(95)<200'], // 95% of requests must complete under 200ms
    },
};

// --- Test Logic ---
export default function () {
    // The TARGET_URL is passed in as an environment variable by the benchmark script
    const target = __ENV.TARGET_URL || 'http://localhost:8000';

    // Group requests for better organization in results
    group('API Endpoints', function () {
        // 90% of the traffic will hit the fast, root endpoint
        const resRoot = http.get(`${target}/`);
        check(resRoot, {
            'root status was 200': (r) => r.status === 200,
        });

        // 10% of the traffic will hit the slower, "heavy" endpoint
        if (__VU % 10 === 0) {
            const resHeavy = http.get(`${target}/heavy`);
            check(resHeavy, {
                'heavy status was 200': (r) => r.status === 200,
            });
        }
    });

    // Wait for a short, random time between requests to simulate real user behavior
    sleep(Math.random() * 0.5 + 0.1);
}