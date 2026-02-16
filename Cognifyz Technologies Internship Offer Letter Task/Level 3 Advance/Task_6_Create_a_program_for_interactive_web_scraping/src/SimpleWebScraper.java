import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.Scanner;

public class SimpleWebScraper {
    public static void main(String[] args) throws Exception {

        Scanner scanner = new Scanner(System.in);

        // "Advanced": We pretend to be a real browser so websites don't block us.
        String userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " +
                "Chrome/91.0.4472.124 Safari/537.36";

        while (true) {
            try {
                System.out.println("\n--- ADVANCED WEB SCRAPER ---");
                System.out.print("Enter website URL (or 'exit' to quit): ");
                String url = scanner.nextLine();

                if (url.equalsIgnoreCase("exit")) break;

                // Step 1 & 2: Connect with User Agent and Timeout
                System.out.println("Connecting to " + url + "...");
                Document doc = Jsoup.connect(url)
                        .userAgent(userAgent)
                        .timeout(10000) // Wait up to 10 seconds
                        .get();

                // Step 3: User-Friendly Presentation (Interactive Menu)
                System.out.println("Connection Successful! Title: " + doc.title());
                System.out.println("What would you like to extract?");
                System.out.println("1. Headlines (h1, h2, h3)");
                System.out.println("2. All Links");
                System.out.println("3. Images");
                System.out.print("Enter choice (1-3): ");

                String choice = scanner.nextLine();
                System.out.println("\n--- RESULTS ---");

                switch (choice) {
                    case "1":
                        // Fetching H1, H2, and H3 tags
                        Elements headers = doc.select("h1, h2, h3");
                        if (headers.isEmpty()) System.out.println("No headlines found.");
                        for (Element h : headers) {
                            // Clean up text
                            System.out.println("[" + h.tagName().toUpperCase() + "] " + h.text());
                        }
                        break;

                    case "2":
                        // Fetching links
                        Elements links = doc.select("a[href]");
                        int linkCount = 0;
                        for (Element link : links) {
                            String linkText = link.text();
                            String linkHref = link.attr("abs:href"); // "abs:href" gives the full http URL

                            // Only print if text is not empty (filters out hidden links)
                            if (!linkText.isEmpty()) {
                                System.out.printf("Text: %-20s | URL: %s%n",
                                        linkText.length() > 20 ? linkText.substring(0, 17) + "..." : linkText,
                                        linkHref);
                                linkCount++;
                            }
                            if (linkCount >= 10) break; // Limit to 10 links to keep it readable
                        }
                        System.out.println("... (Showing top 10 links)");
                        break;

                    case "3":
                        // Fetching images
                        Elements images = doc.select("img[src]");
                        for (Element img : images) {
                            System.out.println("Image: " + img.attr("abs:src"));
                        }
                        break;

                    default:
                        System.out.println("Invalid choice.");
                }

            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
                System.out.println("Make sure the URL starts with http:// or https://");
            }
        }
        scanner.close();
    }
}