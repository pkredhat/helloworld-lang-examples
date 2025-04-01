using System.Text.Json;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using System.IO;
using System.Collections.Generic;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var port = Environment.GetEnvironmentVariable("PORT") ?? "8080";
string? countryCode = Environment.GetEnvironmentVariable("COUNTRY_CODE") ?? "en";

if (string.IsNullOrEmpty(countryCode))
{
    Console.WriteLine("NO Country Code");
}
else
{
    Console.WriteLine($"countryCode: {countryCode}");
}

app.MapGet("/", async (HttpContext context) =>
{
    if (string.IsNullOrEmpty(countryCode))
    {
        context.Response.StatusCode = 400;
        await context.Response.WriteAsync("Country code parameter is required.");
        return;
    }

    try
    {
        string json = await File.ReadAllTextAsync("translations.json");

        // Deserialize into a dictionary that includes "translations"
        var jsonObject = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(json);

        if (jsonObject != null && jsonObject.TryGetValue("translations", out var translations))
        {
            if (translations.TryGetValue(countryCode.ToUpper(), out var translation))
            {
                context.Response.StatusCode = 200;
                await context.Response.WriteAsync(translation);
            }
            else
            {
                context.Response.StatusCode = 404;
                await context.Response.WriteAsync("Translation not found for the specified country code.");
            }
        }
        else
        {
            context.Response.StatusCode = 500;
            await context.Response.WriteAsync("Invalid JSON format.");
        }
    }
    catch (Exception ex)
    {
        context.Response.StatusCode = 500;
        await context.Response.WriteAsync($"Error: {ex.Message}");
    }
});

app.Run($"http://0.0.0.0:{port}");