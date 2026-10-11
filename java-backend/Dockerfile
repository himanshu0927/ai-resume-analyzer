FROM openjdk:25-ea-slim AS build
WORKDIR /app
COPY src ./src
RUN mkdir bin && javac -d bin src/com/ai/resume/Main.java

FROM openjdk:25-ea-slim
WORKDIR /app
COPY --from=build /app/bin ./bin
EXPOSE 8000
CMD ["java", "-cp", "bin", "com.ai.resume.Main"]
