# Use the official .NET SDK image to build the app
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

# Set the working directory
WORKDIR /app

# Copy everything and restore dependencies
COPY . . 
RUN dotnet restore

# Build the application
RUN dotnet publish -c Release -o /out

# Use a smaller runtime image
FROM mcr.microsoft.com/dotnet/runtime:9.0

# Set the working directory in the runtime container
WORKDIR /app

# Copy built files from the previous stage
COPY --from=build /out .

# Set the command to run the app
ENTRYPOINT ["dotnet", "helloworld.net-multilang.dll"]
