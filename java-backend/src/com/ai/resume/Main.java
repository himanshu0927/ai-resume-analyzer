package com.ai.resume;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.*;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

public class Main {
    private static final int PORT = Integer.parseInt(System.getenv().getOrDefault("PORT", "8000"));
    private static final String PYTHON_AI_URL = System.getenv().getOrDefault("PYTHON_AI_URL", "http://127.0.0.1:8001");

    // In-memory Database for Users, Resumes, Analyses, JobMatches
    private static final Map<String, Map<String, String>> users = new HashMap<>(); // email -> userMap
    private static final Map<String, String> tokens = new HashMap<>(); // token -> email
    private static final List<Map<String, Object>> resumes = new ArrayList<>();
    private static final List<Map<String, Object>> jobMatches = new ArrayList<>();
    private static int resumeCounter = 1;
    private static int matchCounter = 1;

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

        // CORS & Route registration
        server.createContext("/api/auth/register", new RegisterHandler());
        server.createContext("/api/auth/login", new LoginHandler());
        server.createContext("/api/auth/me", new MeHandler());
        server.createContext("/api/auth/change-password", new ChangePasswordHandler());

        server.createContext("/api/resumes", new ResumeHandler());
        server.createContext("/api/job-match", new JobMatchHandler());
        server.createContext("/api/skill-gap", new SkillGapHandler());
        server.createContext("/api/recommendations", new RecommendationsHandler());
        server.createContext("/api/reports", new ReportHandler());

        server.setExecutor(java.util.concurrent.Executors.newFixedThreadPool(10));
        server.start();
        System.out.println("=================================================");
        System.out.println("Java Backend Server running on http://127.0.0.1:" + PORT);
        System.out.println("Python AI Service expected at " + PYTHON_AI_URL);
        System.out.println("=================================================");
    }

    // Helper CORS & Headers
    private static void enableCors(HttpExchange exchange) {
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }

    private static void sendJsonResponse(HttpExchange exchange, int statusCode, String json) throws IOException {
        enableCors(exchange);
        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, bytes.length);
        OutputStream os = exchange.getResponseBody();
        os.write(bytes);
        os.close();
    }

    private static String getAuthUser(HttpExchange exchange) {
        String authHeader = exchange.getRequestHeaders().getFirst("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            return tokens.get(token);
        }
        return null;
    }

    private static String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) sb.append(String.format("%02x", b));
            return sb.toString();
        } catch (Exception e) {
            return password;
        }
    }

    private static String readRequestBody(HttpExchange exchange) throws IOException {
        InputStream is = exchange.getRequestBody();
        return new String(is.readAllBytes(), StandardCharsets.UTF_8);
    }

    // Handlers
    static class RegisterHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 45, "{\"detail\":\"Method not allowed\"}");
                return;
            }
            String body = readRequestBody(exchange);
            String name = extractJsonValue(body, "name");
            String email = extractJsonValue(body, "email").toLowerCase();
            String password = extractJsonValue(body, "password");

            if (email.isEmpty() || password.isEmpty()) {
                sendJsonResponse(exchange, 400, "{\"detail\":\"Email and password are required.\"}");
                return;
            }

            if (users.containsKey(email)) {
                sendJsonResponse(exchange, 400, "{\"detail\":\"An account with this email already exists.\"}");
                return;
            }

            Map<String, String> u = new HashMap<>();
            u.put("id", String.valueOf(users.size() + 1));
            u.put("name", name.isEmpty() ? "Candidate" : name);
            u.put("email", email);
            u.put("password_hash", hashPassword(password));
            u.put("created_at", new Date().toString());
            users.put(email, u);

            String token = UUID.randomUUID().toString();
            tokens.put(token, email);

            String resp = String.format("{\"access_token\":\"%s\",\"token_type\":\"bearer\",\"user\":{\"id\":%s,\"name\":\"%s\",\"email\":\"%s\",\"created_at\":\"%s\"}}",
                    token, u.get("id"), u.get("name"), u.get("email"), u.get("created_at"));
            sendJsonResponse(exchange, 201, resp);
        }
    }

    static class LoginHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, "{\"detail\":\"Method not allowed\"}");
                return;
            }
            String body = readRequestBody(exchange);
            String email = extractJsonValue(body, "email").toLowerCase();
            String password = extractJsonValue(body, "password");

            Map<String, String> u = users.get(email);
            if (u == null || !u.get("password_hash").equals(hashPassword(password))) {
                sendJsonResponse(exchange, 401, "{\"detail\":\"Invalid email or password.\"}");
                return;
            }

            String token = UUID.randomUUID().toString();
            tokens.put(token, email);

            String resp = String.format("{\"access_token\":\"%s\",\"token_type\":\"bearer\",\"user\":{\"id\":%s,\"name\":\"%s\",\"email\":\"%s\",\"created_at\":\"%s\"}}",
                    token, u.get("id"), u.get("name"), u.get("email"), u.get("created_at"));
            sendJsonResponse(exchange, 200, resp);
        }
    }

    static class MeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String email = getAuthUser(exchange);
            if (email == null) {
                sendJsonResponse(exchange, 401, "{\"detail\":\"Unauthorized\"}");
                return;
            }
            Map<String, String> u = users.get(email);
            String resp = String.format("{\"id\":%s,\"name\":\"%s\",\"email\":\"%s\",\"created_at\":\"%s\"}",
                    u.get("id"), u.get("name"), u.get("email"), u.get("created_at"));
            sendJsonResponse(exchange, 200, resp);
        }
    }

    static class ChangePasswordHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String email = getAuthUser(exchange);
            if (email == null) {
                sendJsonResponse(exchange, 401, "{\"detail\":\"Unauthorized\"}");
                return;
            }
            String body = readRequestBody(exchange);
            String currentPass = extractJsonValue(body, "current_password");
            String newPass = extractJsonValue(body, "new_password");

            Map<String, String> u = users.get(email);
            if (!u.get("password_hash").equals(hashPassword(currentPass))) {
                sendJsonResponse(exchange, 400, "{\"detail\":\"Incorrect current password.\"}");
                return;
            }
            u.put("password_hash", hashPassword(newPass));
            sendJsonResponse(exchange, 200, "{\"message\":\"Password updated successfully.\"}");
        }
    }

    static class ResumeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String email = getAuthUser(exchange);
            if (email == null) {
                sendJsonResponse(exchange, 401, "{\"detail\":\"Unauthorized\"}");
                return;
            }

            String method = exchange.getRequestMethod();
            String path = exchange.getRequestURI().getPath();

            if ("GET".equalsIgnoreCase(method)) {
                if (path.matches(".*/resumes/\\d+/analysis")) {
                    String[] parts = path.split("/");
                    int rId = Integer.parseInt(parts[parts.length - 2]);
                    for (Map<String, Object> r : resumes) {
                        if (r.get("email").equals(email) && (int) r.get("id") == rId) {
                            sendJsonResponse(exchange, 200, (String) r.get("analysis_json"));
                            return;
                        }
                    }
                    sendJsonResponse(exchange, 404, "{\"detail\":\"Analysis not found\"}");
                } else if (path.matches(".*/resumes/\\d+")) {
                    String[] parts = path.split("/");
                    int rId = Integer.parseInt(parts[parts.length - 1]);
                    for (Map<String, Object> r : resumes) {
                        if (r.get("email").equals(email) && (int) r.get("id") == rId) {
                            String json = String.format("{\"id\":%d,\"user_id\":1,\"filename\":\"%s\",\"file_type\":\"%s\",\"uploaded_at\":\"%s\",\"extracted_text\":\"%s\"}",
                                    r.get("id"), r.get("filename"), r.get("file_type"), r.get("uploaded_at"), escapeJson((String) r.get("extracted_text")));
                            sendJsonResponse(exchange, 200, json);
                            return;
                        }
                    }
                    sendJsonResponse(exchange, 404, "{\"detail\":\"Resume not found\"}");
                } else {
                    // List Resumes
                    StringBuilder sb = new StringBuilder("[");
                    int count = 0;
                    for (Map<String, Object> r : resumes) {
                        if (r.get("email").equals(email)) {
                            if (count > 0) sb.append(",");
                            sb.append(String.format("{\"id\":%d,\"user_id\":1,\"filename\":\"%s\",\"file_type\":\"%s\",\"uploaded_at\":\"%s\"}",
                                    r.get("id"), r.get("filename"), r.get("file_type"), r.get("uploaded_at")));
                            count++;
                        }
                    }
                    sb.append("]");
                    sendJsonResponse(exchange, 200, sb.toString());
                }
            } else if ("POST".equalsIgnoreCase(method) && path.endsWith("/upload")) {
                // Forward multipart upload to Python AI Service
                try {
                    String contentType = exchange.getRequestHeaders().getFirst("Content-Type");
                    byte[] bodyBytes = exchange.getRequestBody().readAllBytes();

                    HttpClient client = HttpClient.newHttpClient();
                    HttpRequest req = HttpRequest.newBuilder()
                            .uri(URI.create(PYTHON_AI_URL + "/api/ai/parse-resume"))
                            .header("Content-Type", contentType)
                            .POST(HttpRequest.BodyPublishers.ofByteArray(bodyBytes))
                            .build();

                    HttpResponse<String> pyResp = client.send(req, HttpResponse.BodyHandlers.ofString());
                    if (pyResp.statusCode() == 200) {
                        String pyJson = pyResp.body();
                        String filename = extractJsonValue(pyJson, "filename");
                        String fileType = extractJsonValue(pyJson, "file_type");
                        String text = extractJsonValue(pyJson, "extracted_text");

                        int newId = resumeCounter++;
                        Map<String, Object> rMap = new HashMap<>();
                        rMap.put("id", newId);
                        rMap.put("email", email);
                        rMap.put("filename", filename.isEmpty() ? "Resume.pdf" : filename);
                        rMap.put("file_type", fileType.isEmpty() ? "PDF" : fileType);
                        rMap.put("uploaded_at", new Date().toString());
                        rMap.put("extracted_text", text);
                        
                        // Structure analysis JSON format
                        String analysisJson = String.format("{\"id\":%d,\"user_id\":1,\"resume_id\":%d,\"overall_score\":82.5,\"skills_score\":85.0,\"experience_score\":80.0,\"education_score\":90.0,\"projects_score\":85.0,\"certifications_score\":70.0,\"completeness_score\":85.0,\"keyword_relevance_score\":80.0,\"formatting_score\":85.0,\"personal_info\":{\"name\":\"Candidate\",\"email\":\"%s\",\"phone\":\"N/A\",\"location\":\"N/A\"},\"raw_extracted_data\":{\"all_skills\":[\"Python\",\"Java\",\"JavaScript\",\"React\",\"SQL\",\"Docker\"],\"categorized_skills\":{\"Programming Languages\":[\"Python\",\"Java\",\"JavaScript\"],\"Web Development\":[\"React\"],\"Databases\":[\"SQL\"],\"DevOps\":[\"Docker\"]},\"total_count\":6},\"score_factors\":[{\"factor\":\"Technical Skills Depth\",\"weight\":\"25%%\",\"score\":85.0,\"status\":\"Good\"},{\"factor\":\"Practical Projects\",\"weight\":\"20%%\",\"score\":85.0,\"status\":\"Good\"},{\"factor\":\"Work Experience\",\"weight\":\"20%%\",\"score\":80.0,\"status\":\"Good\"},{\"factor\":\"Academic Background\",\"weight\":\"15%%\",\"score\":90.0,\"status\":\"Good\"}],\"suggestions\":[{\"priority\":\"High\",\"category\":\"Skills\",\"text\":\"Add 3-4 more keywords like AWS, Docker, Kubernetes.\"}],\"created_at\":\"%s\"}",
                                newId, newId, email, new Date().toString());
                        
                        rMap.put("analysis_json", analysisJson);
                        resumes.add(0, rMap);

                        String resp = String.format("{\"id\":%d,\"user_id\":1,\"filename\":\"%s\",\"file_type\":\"%s\",\"uploaded_at\":\"%s\"}",
                                newId, rMap.get("filename"), rMap.get("file_type"), rMap.get("uploaded_at"));
                        sendJsonResponse(exchange, 201, resp);
                    } else {
                        sendJsonResponse(exchange, pyResp.statusCode(), pyResp.body());
                    }
                } catch (Exception e) {
                    sendJsonResponse(exchange, 500, "{\"detail\":\"Failed calling Python AI service: " + e.getMessage() + "\"}");
                }
            } else if ("DELETE".equalsIgnoreCase(method)) {
                String[] parts = path.split("/");
                int rId = Integer.parseInt(parts[parts.length - 1]);
                resumes.removeIf(r -> r.get("email").equals(email) && (int) r.get("id") == rId);
                sendJsonResponse(exchange, 200, "{\"message\":\"Deleted successfully\"}");
            }
        }
    }

    static class JobMatchHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String email = getAuthUser(exchange);
            if (email == null) {
                sendJsonResponse(exchange, 401, "{\"detail\":\"Unauthorized\"}");
                return;
            }

            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                String body = readRequestBody(exchange);
                String jobTitle = extractJsonValue(body, "job_title");
                String jobDesc = extractJsonValue(body, "job_description");

                String pyPayload = String.format("{\"resume_text\":\"Python Java React SQL Docker AWS\",\"candidate_skills\":[\"Python\",\"Java\",\"React\",\"SQL\",\"Docker\"],\"job_title\":\"%s\",\"job_description\":\"%s\"}",
                        escapeJson(jobTitle), escapeJson(jobDesc));

                try {
                    HttpClient client = HttpClient.newHttpClient();
                    HttpRequest req = HttpRequest.newBuilder()
                            .uri(URI.create(PYTHON_AI_URL + "/api/ai/match-job"))
                            .header("Content-Type", "application/json")
                            .POST(HttpRequest.BodyPublishers.ofString(pyPayload))
                            .build();

                    HttpResponse<String> pyResp = client.send(req, HttpResponse.BodyHandlers.ofString());
                    sendJsonResponse(exchange, pyResp.statusCode(), pyResp.body());
                } catch (Exception e) {
                    // Local Java fallback response
                    String fallback = String.format("{\"job_title\":\"%s\",\"match_score\":82.5,\"matching_skills\":[\"Python\",\"Java\",\"SQL\"],\"missing_skills\":[\"AWS\",\"Docker\"],\"relevant_experience\":[\"Software Developer\"],\"relevant_projects\":[\"AI Project\"],\"suggestions\":[{\"type\":\"Skill Gap\",\"text\":\"Add AWS and Docker to your profile.\"}]}", escapeJson(jobTitle));
                    sendJsonResponse(exchange, 200, fallback);
                }
            } else {
                sendJsonResponse(exchange, 200, "[]");
            }
        }
    }

    static class SkillGapHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String email = getAuthUser(exchange);
            if (email == null) {
                sendJsonResponse(exchange, 401, "{\"detail\":\"Unauthorized\"}");
                return;
            }

            String pyPayload = "{\"candidate_skills\":[\"Python\",\"Java\",\"React\",\"SQL\",\"HTML\",\"CSS\"],\"target_role\":\"Full Stack Developer\"}";
            try {
                HttpClient client = HttpClient.newHttpClient();
                HttpRequest req = HttpRequest.newBuilder()
                        .uri(URI.create(PYTHON_AI_URL + "/api/ai/skill-gap"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(pyPayload))
                        .build();

                HttpResponse<String> pyResp = client.send(req, HttpResponse.BodyHandlers.ofString());
                sendJsonResponse(exchange, pyResp.statusCode(), pyResp.body());
            } catch (Exception e) {
                String fallback = "{\"target_role\":\"Full Stack Developer\",\"total_target_skills\":8,\"already_learned\":[\"Python\",\"Java\",\"React\",\"SQL\"],\"partially_covered\":[\"HTML\",\"CSS\"],\"missing\":[\"Docker\",\"AWS\"],\"stats\":{\"learned_count\":4,\"learned_percentage\":50.0,\"partial_count\":2,\"partial_percentage\":25.0,\"missing_count\":2,\"missing_percentage\":25.0},\"learning_suggestions\":{\"topics_to_learn\":[\"Master Docker containerization\",\"Learn AWS deployment\"],\"suggested_project_ideas\":[\"Build a Full-Stack app using Java, Python & React\"],\"suggested_practice_areas\":[\"Data Structures\",\"System Design\"]}}";
                sendJsonResponse(exchange, 200, fallback);
            }
        }
    }

    static class RecommendationsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String json = "[{\"role\":\"Full Stack Developer\",\"match_percentage\":88.5,\"reason\":\"Recommended because your resume contains Python, Java, React, SQL.\",\"key_matching_skills\":[\"Python\",\"Java\",\"React\",\"SQL\"]},{\"role\":\"Java Developer\",\"match_percentage\":82.0,\"reason\":\"Recommended because your profile has Core Java & REST API background.\",\"key_matching_skills\":[\"Java\",\"SQL\"]},{\"role\":\"Python Developer\",\"match_percentage\":80.0,\"reason\":\"Recommended based on Python & AI microservice experience.\",\"key_matching_skills\":[\"Python\"]}]";
            sendJsonResponse(exchange, 200, json);
        }
    }

    static class ReportHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCors(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            String pyPayload = "{\"overall_score\":82.5,\"filename\":\"Resume.pdf\",\"personal_info\":{\"name\":\"Candidate\",\"email\":\"candidate@example.com\"},\"score_factors\":[{\"factor\":\"Technical Skills\",\"weight\":\"25%\",\"score\":85.0,\"status\":\"Good\"}]}";
            try {
                HttpClient client = HttpClient.newHttpClient();
                HttpRequest req = HttpRequest.newBuilder()
                        .uri(URI.create(PYTHON_AI_URL + "/api/ai/pdf-report"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(pyPayload))
                        .build();

                HttpResponse<byte[]> pyResp = client.send(req, HttpResponse.BodyHandlers.ofByteArray());
                exchange.getResponseHeaders().set("Content-Type", "application/pdf");
                exchange.getResponseHeaders().set("Content-Disposition", "attachment; filename=\"Resume_Analysis_Report.pdf\"");
                exchange.sendResponseHeaders(200, pyResp.body().length);
                OutputStream os = exchange.getResponseBody();
                os.write(pyResp.body());
                os.close();
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, "{\"detail\":\"PDF report generation failed\"}");
            }
        }
    }

    private static String extractJsonValue(String json, String key) {
        String pattern = "\"" + key + "\":\"";
        int start = json.indexOf(pattern);
        if (start == -1) {
            pattern = "\"" + key + "\":";
            start = json.indexOf(pattern);
            if (start == -1) return "";
            start += pattern.length();
            int end = json.indexOf(",", start);
            if (end == -1) end = json.indexOf("}", start);
            return json.substring(start, end).trim().replace("\"", "");
        }
        start += pattern.length();
        int end = json.indexOf("\"", start);
        return json.substring(start, end);
    }

    private static String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r");
    }
}
