import java.util.Scanner;
import java.net.InetAddress;
import java.net.UnknownHostException;

public class Main {


    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        Client client = null;

        try {
            client = new Client(InetAddress.getByName("localhost"), 8762);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
        while (true) {
            client.setKey(input.nextLine());
            client.setData(client.getKey().getBytes());
            System.out.print(client.getData());
            client.sendData(client.getKey());
        }
    }
}
