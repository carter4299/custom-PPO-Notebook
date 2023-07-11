package org.example;
import org.kohsuke.github.*;
import java.io.*;
import java.net.*;
import org.kohsuke.github.GHContent;
import org.kohsuke.github.GHRepository;
import org.kohsuke.github.GitHub;

public class Main {

    public static String get_text() throws IOException {
        URL path1 = new URL("https://stockanalysis.com/stocks/");URLConnection con = path1.openConnection();InputStream is = con.getInputStream();BufferedReader br = new BufferedReader(new InputStreamReader(is));
        String line = null;

        while ((line = br.readLine()) != null) {

            if (line.contains("const data")) {
                line = line.replace("\t\t\t\t\tconst data = [{\"type\":\"data\",\"data\":{session:null,loc:{co:\"US\",isUS:true,isEU:false,isCA:false},theme:void 0},\"uses\":{}},{\"type\":\"data\",\"data\":{data:[", "");
                line = line.replace("]},\"uses\":{}}];", "");
                return line;
            }
        }
        return null;
    }

    public static void update_github_file(String content) throws IOException {
        String repoName = "carter4299/custom-PPO-Notebook";
        String path = "market_cap_updater/stockanalysis.txt";
        String message = "Updating file";

        GitHub github = new GitHubBuilder().withOAuthToken(System.getenv("GITHUB_TOKEN")).build();
        GHRepository repo = github.getRepository(repoName);

        GHContent fileContent = repo.getFileContent(path);
        if (fileContent != null) {
            fileContent.update(content, message);
        } else {
            // file does not exist - create a new one
            repo.createContent(content, message, path);
        }
    }

    public static void main(String[] args) throws FileNotFoundException, IOException {
        String text = get_text();
        if(text != null){
            update_github_file(text);
        }
    }
}
