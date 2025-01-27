# Stage 1: Build the application
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app

# Copy only the necessary files for dependency resolution first
COPY pom.xml .
RUN mvn dependency:go-offline

# Now copy the rest of the source code
COPY src ./src

# Build the application (create the jar file)
RUN mvn clean package -DskipTests

# Stage 2: Create the final image
FROM openjdk:17-jdk-slim
WORKDIR /app

# Copy the JAR file from the build stage (use the correct jar file name)
COPY --from=build /app/target/aspicedev-1.0-SNAPSHOT.jar /app/aspicedev-1.0-SNAPSHOT.jar

# Print the Java version to ensure Java is available
RUN java -version

# List files in the working directory to verify the JAR file is present
RUN ls -lh /app

# Expose port 80
EXPOSE 80

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=5 CMD curl -f http://localhost/ || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "/app/aspicedev-1.0-SNAPSHOT.jar"]
